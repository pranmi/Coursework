voltage <- read.csv("VOLTAGE.csv")#read in VOLTAGE.csv
#separating datasets by location for comparison
loc0 <- subset(voltage, location == "0")[["voltage"]]
loc1 <- subset(voltage, location == "1")[["voltage"]]
#Also only taking voltage values since location is a redundant column once they are separated
#Comparing summary stats as part of EDA (Exploratory Data Analysis)
summary(loc0)
summary(loc1)
#For graphical EDA, going to plot the two side by side boxplot

voltage <- read.csv("VOLTAGE.csv")#read in VOLTAGE.csv
#separating datasets by location for comparison
loc0 <- subset(voltage, location == "0")[["voltage"]]
loc1 <- subset(voltage, location == "1")[["voltage"]]
#Also only taking voltage values since location is a redundant column once they are separated
#Comparing summary stats as part of EDA (Exploratory Data Analysis)
summary(loc0)
summary(loc1)
#For graphical EDA, going to plot the two side by side boxplot
boxplot(loc0, loc1,
        names = c("Location 0", "Location 1"),
        main = "Voltage Comparison by Location",
        ylab = "Voltage")
#Start of part 1b
library(BSDA)#For the z.test function
#Note: Using alpha of .05 since none given and .05 is common
alpha <- .05
t.test(loc0, loc1, alternative = "two.sided", conf.level = 1 - alpha)
#Start of Question 2:
vapor <- read.csv("VAPOR.csv") #Reading in data
names(vapor)
theoretical <- vapor[["theoretical"]] #Separating data into two samples
experimental <- vapor[["experimental"]] #To be compared in hypothesis testing
#Running two sample t-test, two sided, with confidence of 95% 
#H0 being that theoretical & experimental ~ same distribution (i.e. theoretical model is accurate)
t.test(theoretical, experimental, alternative = "two.sided", conf.level = .95)
