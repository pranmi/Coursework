import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
from itertools import product
import numpy as np
import time
import sys

sys.stdout.reconfigure(line_buffering=True)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
TUNE_EPOCHS = 5
FINAL_EPOCHS = 20

def get_datasets(name):
    if name == "MNIST":
        MNIST_TRANSFORM = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])

        train_full = datasets.MNIST("data", train=True, download=True, transform=MNIST_TRANSFORM)
        test = datasets.MNIST("data", train=False, download=True, transform=MNIST_TRANSFORM)
    elif name == "CIFAR10":
        CIFAR_TRANSFORM = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.4914, 0.4822, 0.4465],
                                std=[0.2470, 0.2435, 0.2616])
        ])
        train_full = datasets.CIFAR10("data", train=True, download=True, transform=CIFAR_TRANSFORM)
        test = datasets.CIFAR10("data", train=False, download=True, transform=CIFAR_TRANSFORM)
    else:
        raise ValueError("Unknown dataset")
    return train_full, test

def make_train_val_split(train_full, dataset_name):
    if dataset_name == "MNIST":
        train_size, val_size = 50000, 10000
    elif dataset_name == "CIFAR10":
        train_size, val_size = 45000, 5000
    else:
        raise ValueError("Unknown dataset")
    assert train_size + val_size == len(train_full), "Split sizes must sum to dataset length"
    generator = torch.Generator()
    train_set, val_set = random_split(train_full, [train_size, val_size], generator=generator)
    return train_set, val_set

class MLP(nn.Module):
    def __init__(self, input_dim, hidden_layers, num_classes=10, dropout=0.0):
        super().__init__()
        layers = []
        prev = input_dim
        for h in hidden_layers:
            layers.append(nn.Linear(prev, h))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            prev = h
        layers.append(nn.Linear(prev, num_classes))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x.view(x.size(0), -1))

def train_one_epoch(model, loader, opt, loss_fn):
    model.train()
    total_loss = 0
    for x, y in loader:
        x, y = x.to(DEVICE), y.to(DEVICE)
        opt.zero_grad()
        preds = model(x)
        loss = loss_fn(preds, y)
        loss.backward()
        opt.step()
        total_loss += loss.item() * x.size(0)
    return total_loss / len(loader.dataset)

def evaluate(model, loader):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for x, y in loader:
            x, y = x.to(DEVICE), y.to(DEVICE)
            preds = model(x)
            correct += (preds.argmax(1) == y).sum().item()
            total += y.size(0)
    return correct / total

def tune_model(dataset_name, hidden_layers, lr, batch_size, optimizer_name, dropout, epochs=TUNE_EPOCHS):
    train_full, _ = get_datasets(dataset_name)
    train_set, val_set = make_train_val_split(train_full, dataset_name)
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=batch_size)

    input_dim = torch.numel(train_full[0][0])
    model = MLP(input_dim, hidden_layers, 10, dropout).to(DEVICE)
    loss_fn = nn.CrossEntropyLoss()

    opt = optim.Adam(model.parameters(), lr=lr) if optimizer_name == "Adam" else \
          optim.SGD(model.parameters(), lr=lr, momentum=0.9)

    best_val = 0
    start = time.time()
    for _ in range(epochs):
        train_one_epoch(model, train_loader, opt, loss_fn)
        val_acc = evaluate(model, val_loader)
        best_val = max(best_val, val_acc)
    runtime = (time.time() - start) / 60
    return best_val, runtime

def train_final_model(dataset_name, hidden_layers, lr, batch_size, optimizer_name, dropout, epochs=FINAL_EPOCHS):
    train_full, test = get_datasets(dataset_name)
    train_loader = DataLoader(train_full, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test, batch_size=batch_size)

    input_dim = torch.numel(train_full[0][0])
    model = MLP(input_dim, hidden_layers, 10, dropout).to(DEVICE)
    loss_fn = nn.CrossEntropyLoss()
    opt = optim.Adam(model.parameters(), lr=lr) if optimizer_name == "Adam" else \
          optim.SGD(model.parameters(), lr=lr, momentum=0.9)

    for _ in range(epochs):
        train_one_epoch(model, train_loader, opt, loss_fn)
    test_acc = evaluate(model, test_loader)
    return test_acc


if __name__ == "__main__":
    ARCHITECTURES = {
    "Shallow": [128],
    "Medium": [512, 256, 128],
    "Deep": [1024, 512, 256, 128, 64]
    }

    LEARNING_RATES = [1e-2, 1e-3, 1e-4]
    BATCH_SIZES = [32, 64, 128]
    OPTIMIZERS = ["SGD", "Adam"]
    DROPOUTS = [0.2, 0.5]


    for dataset_name in ["MNIST", "CIFAR10"]:
        print(f"\n==================== {dataset_name} ====================\n")
        for arch_name, hidden_layers in ARCHITECTURES.items():
            print(f"\n--- Architecture: {arch_name} ({hidden_layers}) ---")
            results = []
            for lr, bs, opt, drop in product(LEARNING_RATES, BATCH_SIZES, OPTIMIZERS, DROPOUTS):
                val_acc, rt = tune_model(dataset_name, hidden_layers, lr, bs, opt, drop, TUNE_EPOCHS)
                results.append({
                    "lr": lr, "bs": bs, "opt": opt, "drop": drop,
                    "val_acc": val_acc, "runtime": rt
                })

        best = max(results, key=lambda x: x["val_acc"])

        print("\nFinal Tuned Model Results:\n")
        print(f"{'Learning Rate':<14}{'Batch Size':<12}{'Optimizer':<10}{'Dropout':<10}"
            f"{'Validation Acc':<18}{'Runtime (min)':<14}")
        print("-" * 78)
        print(f"{best['lr']:<14}{best['bs']:<12}{best['opt']:<10}{best['drop']:<10}"
            f"{best['val_acc']*100:6.2f}{'':<9}{best['runtime']:14.2f}")

        train_full, test_set = get_datasets(dataset_name)
        full_loader = DataLoader(train_full, batch_size=best["bs"], shuffle=True)
        test_loader = DataLoader(test_set, batch_size=best["bs"])

        input_dim = torch.numel(train_full[0][0])
        final_model = MLP(input_dim, hidden_layers, 10, best["drop"]).to(DEVICE)
        loss_fn = nn.CrossEntropyLoss()
        opt = optim.Adam(final_model.parameters(), lr=best["lr"]) if best["opt"] == "Adam" \
            else optim.SGD(final_model.parameters(), lr=best["lr"], momentum=0.9)

        for _ in range(FINAL_EPOCHS):
            train_one_epoch(final_model, full_loader, opt, loss_fn)

        test_acc = evaluate(final_model, test_loader)
        print(f"\nFinal Test Accuracy: {test_acc*100:.2f}%\n")