# Data Analysis for the Social Sciences Presentation 3
# Author: Xu (Conan) Huang
# Topics: Linear and non-linear regression and Confidence Interval

from __future__ import division

### Education and occupational prestige (slide 4)

## explore the dataset and plot data

# One way to graph the plot is to use NumPy
import numpy as np      # numpy is the numerical module that allows you to do Matlab-esque numerical operations
import matplotlib      # matplotlib is a (primarily 2D) desktop plotting package designed for creating publication-quality plots
import matplotlib.pyplot as plt   # pyplot (part of matplotlib) is the plotting library

# Load the dataset (replace the 'path' with your own path to directory)
data = np.genfromtxt('C:/Users/Conan/Desktop/prestige.csv', skiprows=1, delimiter=',') 
data
type(data)  # the dataset is a numpy n-dimensional array
x = data[:,1]   # create separate arrays for each column
y = data[:,2]

plt.figure()    # create a new empty plot
plt.plot(x, y, 'b.',linewidth = 0) # Plot the data values. Syntax is pyplot.plot(xarray, yarray, other kwargs)
plt.axis([9, 18, 30, 70])   # set the range for x-axis and y-axis
plt.title('Plotting occupational prestige against education')  # add title and labels
plt.xlabel('Education in years')
plt.ylabel('Prestige')
plt.grid(True)
plt.show()  # Plot simply creates a plot object. To view it, you need to either show or savefig, such as plt.savefig('prestige_plot.png',dpi=100)

# Another way (easier way) is to use Pandas (Pandas is short for panel data)
import pandas as pd
df = pd.read_csv('C:/Users/Conan/Desktop/prestige.csv')
df.head()   # check the first 5 lines
type(df)   # the dataset is a DataFrame 
df.columns  # display column names
df.shape    # display the dimension of the DataFrame
df.plot(kind = 'scatter', x = 'EDUC', y = 'PRESTG80')
plt.title('Plotting occupational prestige against education')  # add title and labels
plt.xlabel('Education in years')
plt.ylabel('Prestige')

## run simple linear regression (slide 29)

# import Statsmodels library
import statsmodels.api as sm
import statsmodels.formula.api as smf

# create a fitted simple linear regression model and 
# print a comprehensive OLS regression result
lm = smf.ols(formula = 'PRESTG80~EDUC', data = df).fit()
print lm.summary()

# Quantities of interest can be extracted directly from the fitted model.
# Type dir(lm) for a full list of attributes to access. Below are some examples: 
dir(lm)

# print the coefficients
lm.params

# print the intercept
lm.params[0]

# calculate the intercept manually  (a = ybar - b * xbar)
df["PRESTG80"].mean() - lm.params[1] * df["EDUC"].mean()

# print the p-values for the model coefficients
lm.pvalues

# print the R-squared value for the model
lm.rsquared

# print the adjusted R-squared value for the model
lm.rsquared_adj

# print correlation between EDUC and PRESTG80  (slide 33)
r = df['EDUC'].corr(df['PRESTG80'])

# calculate manually
df["EDUC"].std()/df["PRESTG80"].std() * lm.params[1]

# pairwise correlation of DataFrame columns
df.corr()

# calculate Coefficient of Determination
R_2 = r * r

# ANOVA output to calculate R-sq  (slide 54)
lm = smf.ols(formula = 'PRESTG80~EDUC', data = df).fit()
print(sm.stats.anova_lm(lm, typ = 1))

# A regression with no Xs  (slide 56) (gives wrong intercept)
lm_2 = smf.ols(formula = 'PRESTG80~PRESTG80', data = df).fit()
print lm_2.summary()

# the intercept from an 'empty' model (slide 58)
df["PRESTG80"].mean()

# Produce the 95% confidence interval (slide 97)
conf_95 = lm.conf_int(alpha = 0.05)
conf_95.columns = ["2.5%", "97.5%"]
conf_95

# Pearson test for correlation between paired samples (slide 99)
import scipy 
scipy.stats.pearsonr(df["EDUC"], df["PRESTG80"]) # the 1st number is the correlation coefficient, and the latter is p-value

df.corr(method = 'pearson')

# Calculate standard error of the occupational prestige in the sample (slide 102)
df["PRESTG80"].std() / np.sqrt(9)

# run simple linear regression (slide 107)
GSS = pd.read_csv("C:/GSS/GSS_Cum.csv")
d = GSS[GSS.year == 2010]
spank_lm = smf.ols(formula = 'spanking ~ degree', data = d).fit()
print spank_lm.summary()

# dummy independent variable (slide 111)
dummies = pd.get_dummies(d.race)
d["white"] = pd.Series(dummies[1])

num_temp = {}
for num, num_data in d.groupby("white"):
    num_temp[num] = len(num_data)
num_temp

d["white_num"] = 1
pd.pivot_table(d, index = ["white"], values = ["white_num"], aggfunc = np.sum, fill_value = 0)

# cross-tabulation (slide 111)
pd.crosstab(d["white"],d["race"])
pd.crosstab(d["white"],d["race"]).apply(lambda x: x/x.sum(), axis = 1)

# run simple linear regression (slide 112)
tv_lm = smf.ols(formula = "tvhours ~ white", data = d).fit()
print tv_lm.summary()

