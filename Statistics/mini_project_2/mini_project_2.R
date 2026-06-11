race <- read.csv("roadrace.csv")#read in race file

maine_count <- table(race$Maine) #getting number of Main runners for barplot

barplot(maine_count, main = "Runners from Maine vs Away", xlab = "Group", ylab = "Count", col = c("skyblue", "orange"))
#bar plot for part a
#creating subsets for the two groups of runners
maine <- subset(race, Maine == "Maine")
away <- subset(race, Maine == "Away")
names(race) #double checking what each column is referenced as
# Getting times for each group
time_all   <- race[["Time..minutes."]]
time_maine <- maine[["Time..minutes."]]
time_away  <- away[["Time..minutes."]]

# Looked at table to get upper bound, could have also used fastest time as lower bound
breaks <- seq(min(0),
              max(160),
              by = 2)

# Get counts first (so same y-axis)
h1 <- hist(time_maine, plot=FALSE)
h2 <- hist(time_away, plot=FALSE)

# Plotting histograms side by side (thought this part was supposed to be side by side as well)
par(mfrow=c(1,2))

hist(time_maine, #First histogram for Maine runners
     breaks=breaks,
     xlim=range(breaks),
     ylim=c(0, 500),
     main="Maine Runners",
     xlab="Time (minutes)",
     col="skyblue")

hist(time_away, #Second histogram for Away runners
     breaks=breaks,
     xlim=range(breaks),
     ylim=c(0, 500),
     main="Away Runners",
     xlab="Time (minutes)",
     col="orange")

#Summary Stats for each
mmean = mean(time_maine)
msd = sd(time_maine)
mrange = max(time_maine) - min(time_maine)
mmedian = median(time_maine)
mIQR = IQR(time_maine)

amean = mean(time_away)
asd = sd(time_away)
arange = max(time_away) - min(time_away)
amedian = median(time_away)
aIQR = IQR(time_away)

par(mfrow=c(1,1)) #returning to normal plot format for boxplot
boxplot(time_maine, time_away,
        names = c("Maine", "Away"),
        col = c("skyblue", "orange"),
        main = "Race Times: Maine vs Away",
        ylab = "Time (minutes)")

#For part d:
male <- subset(race, Sex == "M")
female <- subset(race, Sex == "F")
#get ages by group
male_age <- male[["Age"]]
female_age <-female[["Age"]]

boxplot(Age ~ Sex, #use age and Sex to create both boxplots
        data = race,
        col = c("lightblue", "lightpink"),
        main = "Runners' Ages by Sex",
        xlab = "Sex",
        ylab = "Age (years)")
#Summary statisitcs for both groups
malemean = mean(male_age)
malesd = sd(male_age)
malerange = max(male_age) - min(male_age)
malemedian = median(male_age)
maleIQR = IQR(male_age)

femalemean = mean(female_age)
femalesd = sd(female_age)
femalerange = max(female_age) - min(female_age)
femalemedian = median(female_age)
femaleIQR = IQR(female_age)

#Part 2
crash_data <- read.csv("motorcycle.csv")
names(crash_data) #just checking column names
boxplot(crash_data[["Fatal.Motorcycle.Accidents"]],
        names = c("Counties"),
        col = c("darkorchid4"),
        main = "Fatal Motorcycle Accidents per county",
        ylab = "Fatal Motorcycle Accidents")
#Summary statistics
crashes <- crash_data[["Fatal.Motorcycle.Accidents"]]
mean <- mean(crashes)
sd <- sd(crashes)
median <- median(crashes)
IQR <- IQR(crashes)
range <- max(crashes) - min(crashes)

#For part 3 b
x <- c(21.72, 14.65, 50.42, 28.78, 11.23)
n <- length(x)

g <- function(theta){
  n/theta - sum((x^theta * log(x)) / (x^theta + 1))
}

result <- uniroot(g, lower = 0.0, upper = 1.0)
result$root
