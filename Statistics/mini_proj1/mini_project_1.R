#Assigning the given probabilities
p_main <- .01
p_backup <- .02
#Calculating how likely it is that they all fail
p_total_failure <- p_main * p_backup * p_backup #All independent and two backups
p_saved <- 1 - p_total_failure
#Compliment of total failure is chance of success

#Q1 PartB: Need to get all combinations of 10 choose 3
folder_possibilities <- combn(10, 3) #all possible combinations
num_possibilities <- ncol(folder_possibilities)

#Q1 PartC:
#Need probability of exactly two refurbs given sampling without replacement
#Can use hypergeometric for this
dhyper(2, 5, 15, 6) #2 "successes", 5 total refurbs, 15 non refurbs, 6 samples without replacement

#Q2 PartA:
#Need to calculate P(arrive on time | depart on time)
p_depart = .9
p_arrive = .8
p_departarrive = .75
#P(arrive|depart) = (P(arrive and depart) / P(depart))
p_arrive_given_depart = p_departarrive/p_depart

#Q2 PartB:
#Continuing use of variables from part A
#Just divide by arrive instead this time since it's flipped
p_depart_given_arrive = p_departarrive/p_arrive

#Q2 PartC:
#Can check if the probability of both occurring matches p(a) * p(d)
p_assume_indep = p_depart * p_arrive
all.equal(p_assume_indep, p_departarrive)


#Q3
#Choice a possible profit and risk
num_shares_a <- 10000/20 # $10000 / $20 per share
profit_a <- num_shares_a * 1 #expected return is $1 profit
var_a <- num_shares_a^2 * (0.5)^2 #total variance is total number of samples (shares) squared times standard deviation squared
num_shares_b <- 10000/50 # $10000 / $50 per share
profit_b <- num_shares_b * 2.5 # $2.5 return expected per share
var_b <- num_shares_b^2 * 1^2 #total variance is total number of samples (shares) squared times standard deviation squared
#Lastly we add half each's profit for the invest 5k in both case, and recalc the variance accordingly
profit_ab <- profit_a/2 + profit_b/2 # expected profit is directly proportional to investment, so we can add half of the totals for each
var_ab <- ((num_shares_a/2)^2 * (0.5)^2) + ((num_shares_b/2)^2 * 1^2) #new calc for var adding both and using half the total shares

#Q4 Part A:
#Expectation for Poisson is simply 1/lambda
lambda <- 3 #jobs per hour
print_expectation <- 60/lambda #Using 60 minutes for 1 hour

#Q4 Part B:
#Can use the poisson cumulative function to get chance
t <- 5/60
mu <- lambda * t #get lambda for the time window
1 - ppois(0, mu) #compliment of cdf is chance that anything is sent in that time
