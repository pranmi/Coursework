bodyheart <- read.csv("bodytemp-heartrate.csv") #read in csv file
names(bodyheart) #just incase column names have some special format/char
#seperate into male and female datasets
male <- subset(bodyheart, gender == "1", select = c("body_temperature", "heart_rate"))
female <- subset(bodyheart, gender == "2", select = c("body_temperature", "heart_rate"))
#Starting Part 1a, EDA
#comparing summary
summary(male["body_temperature"])
summary(female["body_temperature"])
#For graphical EDA, boxplot
boxplot(male$body_temperature, female$body_temperature,
        names = c("Male", "Female"),
        main = "Body temerature vs gender",
        ylab = "body_temperature")
#For hypothesis test
#n > 30 for both so z test, only care about difference so two tailed
library(BSDA)#For the z.test function
z.test(
  x = male$body_temperature,
  y = female$body_temperature,
  alternative = "two.sided",
  sigma.x = sd(male$body_temperature),
  sigma.y = sd(female$body_temperature)
)
#Part 1b, copy and paste of 1a but for heartrate instead
#comparing summary
summary(male["heart_rate"])
summary(female["heart_rate"])
#For graphical EDA, boxplot
boxplot(male$heart_rate, female$heart_rate,
        names = c("Male", "Female"),
        main = "Heart rate vs gender",
        ylab = "Heart rate")
#For hypothesis test
#n > 30 for both so z test, only care about difference so two tailed
z.test(
  x = male$heart_rate,
  y = female$heart_rate,
  alternative = "two.sided",
  sigma.x = sd(male$heart_rate),
  sigma.y = sd(female$heart_rate)
)
#For part 1c: going to get r value and also graph to come up with hypothesis
r <- cor(bodyheart$body_temperature, bodyheart$heart_rate)
#Relatively weak r, so assuming not a strong linear correlation
#Following up with scatterplot
plot(bodyheart$body_temperature, bodyheart$heart_rate, main = "Body temp vs Heart rate",
     xlab = "Body temp", ylab = "heart rate")

#Part 2
cancer <- read.csv("prostate_cancer.csv")
cancer$vesinv <- as.factor(cancer$vesinv)
model <- lm(psa ~ cancervol + weight + age + benpros + vesinv + capspen + gleason, data=cancer)
quant_means <- colMeans(cancer[, c("cancervol", "weight", "age", "benpros", "capspen", "gleason")])
vesinv_mode <- names(sort(table(cancer$vesinv), decreasing = TRUE))[1]
mean_patient <- data.frame(
  cancervol = quant_means["cancervol"],
  weight = quant_means["weight"],
  age = quant_means["age"],
  benpros = quant_means["benpros"],
  vesinv = factor(vesinv_mode, levels = levels(cancer$vesinv)),
  capspen = quant_means["capspen"],
  gleason = quant_means["gleason"]
)
pred_psa <- predict(model, mean_patient)
