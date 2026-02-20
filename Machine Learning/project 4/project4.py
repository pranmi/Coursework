import sklearn.datasets
import sklearn.cluster
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.patches import Ellipse

def plot_gmm_ellipses(X, gmm, predictions, title="GMM Clustering"): #method for plotting elipses for GMM
    plt.figure(figsize=(6,5))
    sns.scatterplot(x=X[:,0], y=X[:,1], hue=predictions.astype(str), palette="tab10", s=60, edgecolor='k') #init the scatterplot using X as the datapoints

    for mean, cov in zip(gmm.means_, gmm.covariances_):
        if cov.ndim == 1:  
            width, height = 2 * np.sqrt(cov) #If the cov is axis alligned, angle = 0 and get width and height with sqrt
            angle = 0.0
        else:  #Otherwise, need to compute it
            v, w = np.linalg.eigh(cov)
            order = v.argsort()[::-1]
            v, w = v[order], w[:, order]
            angle = np.degrees(np.arctan2(w[1,0], w[0,0]))
            width, height = 2 * np.sqrt(v)

        ell = Ellipse(mean, width, height, angle=angle, edgecolor='black', facecolor='none', lw=2)
        plt.gca().add_patch(ell)

    plt.title(title)
    plt.legend(title="Cluster")
    plt.show()

def plot_clusters_seaborn(X, predictions, model=None, title="Clustering Result"): #for the kmeans plot
    df = pd.DataFrame(X, columns=['x', 'y'])
    df['cluster'] = predictions.astype(str)  #turn into a dataframe to make easier

    plt.figure(figsize=(6,5))
    sns.scatterplot(data=df, x='x', y='y', hue='cluster', palette='tab10', s=60, edgecolor='k') #bse the color on the cluster to make clear

    if model is not None and hasattr(model, 'cluster_centers_'):
        centers = model.cluster_centers_ #get the cluster centroids from the model
        plt.scatter(centers[:,0], centers[:,1], c='black', s=200, marker='X', label='Centers') #mark the centers with a black X

    plt.title(title)
    plt.legend(title='Cluster')
    plt.show()

def main():
    shape = -1
    shape = int(input("1.Blob \n2.Moon\n")) - 1
    while(shape not in {0, 1}):
        shape = int(input("Invalid input \n1.Blob \n2.Moon\n"))
    model = -1
    model = int(input("1.K-Means Clustering \n2.GaussianEM\n")) #some basic logic for selecting which model and cluster shape
    while(model not in {1, 2}):
        model = int(input("Invalid input, choose 1 or 2\n"))
    clusters = {2, 3, 4, 5}
    init = {'random', 'k-means++'} #possible hyperparameter space for both models
    covar = {'full', 'diag'}
    if(shape == 0):
        X, y = sklearn.datasets.make_blobs(n_samples=200) #create the dataset based on the selected shape
    else:
        X, y = sklearn.datasets.make_moons(n_samples=200)
    if model == 1:
        for c in clusters:
            for i in init:
                kmeans = sklearn.cluster.KMeans(n_clusters=c, init=i).fit(X) #Create the model to fit the data
                predictions = kmeans.predict(X) #use it to make predictions
                score = silhouette_score(X, predictions) #score those for the silhouette score
                print(f"KMeans with {c} components and {i} initialization done. Silhouette Score: {score:.3f}") #Print those results along with which model this is
                plot_clusters_seaborn(X, predictions, model=kmeans, title=f"K-Means: {c} clusters, init={i}\nSilhouette Score: {score:.3f}") #Call the plotting method to make the plot
    else: #Exact same as the kmeans part above, just some added metric calculations and the different plotting method
        for c in clusters:
            for var in covar:
                gaussEM = GaussianMixture(n_components=c, covariance_type=var).fit(X)
                predictions = gaussEM.predict(X)
                score = silhouette_score(X, predictions)
                avg_log_likelihood = gaussEM.score(X) 
                bic_value = gaussEM.bic(X)
                print(f"Gaussian EM with {c} components and {var} covariance done. Silhouette Score: {score:.3f}, avgLL: {avg_log_likelihood:.3f}, BIC: {bic_value:.3f}")
                plot_gmm_ellipses(X, gaussEM, predictions, title=f"GMM Clustering\nSilhouette Score: {score:.3f}")

if __name__ == "__main__":
    main()