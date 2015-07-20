# Data Analysis for the Social Sciences Presentation 4B
# Author: Xu (Conan) Huang
# Topics: Omitted variables, and multiple regression

from __future__ import division  # In Python 2.x to allow the default floor division operation of / be replaced by true division
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import os
import matplotlib.pyplot as plt

### Do movies that "showcase" women earn less money at the box office?  (slide 20)
#### The Bechdel Test ####
os.chdir("C:/Users/Conan/Desktop")  # change to your own path to directory
d = pd.read_csv("movies-bechdel.csv")

# create new columns in the DataFrame  (slide 24)
d["tg13"] = d["domgross_2013$"] + d["intgross_2013$"]
d["tot_gross_13_mil"] = d["tg13"] / (1000000)
d["budget_13_mil"] = d["budget_2013$"] / (1000000)

# summmary of newly created columns
d["tot_gross_13_mil"].describe()

a = d["tot_gross_13_mil"].describe()  # if you want the result to be rounded to 3 decimal places
a.map(lambda e: round(e, 3))

d["budget_13_mil"].describe()

d["tg13"].describe()

## tabulate the variable "binary"

# one way is to create a dictionary
binary_temp = {}
for a, a_table in d.groupby("binary"):
    binary_temp[a] = len(a_table)
binary_temp
    
# another way is to create a table by using Pandas' "pivot_table"
d["binary_num"] = 1
pd.pivot_table(d, index = ["binary"], values = ["binary_num"], aggfunc = np.sum, fill_value = 0) # "fill_value = 0" replaces missing values with 0

# simple linear regression regarding total gross revenue and pasing/failing the Bechdel test  (slide 25)
lm1 = smf.ols(formula = 'tot_gross_13_mil~binary',data = d).fit()
print lm1.summary()

lm1.resid.describe().map(lambda e: round(e,1))  # Display quantiles of residuals 

# create a summary table  (slide 27)
pd.pivot_table(d, index = "binary", values = "tot_gross_13_mil", aggfunc = [np.mean, np.median])

## Why would a film that showcases women earn so much less money than otherwise?

# multiple linear regression to test spuriousness in the model (slide 31)
lm2 = smf.ols(formula = "tot_gross_13_mil ~ binary + budget_13_mil", data = d).fit()
print lm2.summary() 
lm2.resid.describe().map(lambda f: round(f,1))

# create a summary table  (slide 38)
d.budget_13_mil.describe()

d["budget_cat_num"] = 1
pd.pivot_table(d, index = "budget_cat", values = "budget_cat_num", aggfunc = np.sum)

d["budget_cat"] = pd.cut(d.budget_13_mil, bins = [-1, 16.0700, 37, 78.34, 462], labels = ["low", "some", "lots", "tons"])
pd.pivot_table(d, index = "budget_cat", values = "budget_13_mil", aggfunc = [np.mean, np.median])

# create two subsets and summary tables (slide 39)
passers = d[d["binary"] == "PASS"]  
failers = d[d["binary"] == "FAIL"]
pd.pivot_table(failers, index = "budget_cat", values = "tot_gross_13_mil", aggfunc = [np.mean, np.median])
pd.pivot_table(passers, index = "budget_cat", values = "tot_gross_13_mil", aggfunc = [np.mean, np.median])

# graph (slide 40) (continue to work on it)
data = {'binary': ['FAIL','FAIL','FAIL','FAIL','FAIL','PASS','PASS', 'PASS', 'PASS', 'PASS'], 'budget': ['low','some','lots','tons','total','low','some','lots','tons','total'], 'tot.gross':[106.2490, 199.5900, 322.6565, 590.5176, 330.9495, 67.53362, 169.22763, 271.09875, 615.31012,247.7284]}
df1 = pd.DataFrame(data)
df1.plot(kind = 'barh', x = 'budget', y = 'tot.gross')

# additional information (slide 43)
binary_dict = {"PASS":1, "FAIL":0}
d["pass"] = d["binary"].map(binary_dict.get)
pd.pivot_table(d, index = "budget_cat", values = "pass", aggfunc = np.mean)

# simple linear regression regarding film budget and passing/failing the Bechdel test (slide 46)
lm3 = smf.ols(formula = "budget_13_mil ~ binary", data = d).fit()
print lm3.summary()

### Does marriage make you smarter? (slide 49)

# simple linear regression after removing the missing value in the variable degree (slide 52)
os.chdir("C:/GSS")
d = pd.read_csv("GSS_Cum.csv")

d["married"] = pd.get_dummies(d['marital'])[1.0]
f = d.dropna(subset = ["degree"])   # Notice "dropna" method only creates a copy, does not affect the original dataset
mwlml = smf.ols(formula = "wordsum ~ married", data = f).fit()
print mwlml.summary()
mwlml.resid.describe().map(lambda x: round(x,4))

# multiple linear regression to control for socioeconomic status (proxied by 'degree')  (slide 59)
mwlm2 = smf.ols(formula = "wordsum ~ married + degree", data = d).fit()
print mwlm2.summary()
mwlm2.resid.describe().map(lambda x: round(x,4))

# multiple linear regression that includes the effect of spouse's years of education (slide 67)
lm = smf.ols(formula = "wordsum ~ educ + speduc", data = d).fit()
print lm.summary()

### Do people express lower levels of happiness after the Great Recession (slide 71)

# some recodings  (slide 73)
GSS06and10 = d[d["year"] == 2010]
GSS06and10["rhappy"] = 4 - GSS06and10.happy
# Pandas' Categorical function is similar to R's factor method
rhappy_temp = pd.Series(pd.Categorical(GSS06and10["rhappy"], categories = [1, 2, 3], ordered = True))
# However, it's not possible with Categorical function to specify labels at creation time. Use s.cat.rename_categories(new_labels) afterwards
GSS06and10["rhappy.fact"] = rhappy_temp.cat.rename_categories(["unhappy", "so-so", "happy"]).values

# simple linear regression (slide 74)
b = GSS06and10[["rhappy","year","marital","satfin","hapmar", "health", "satjob"]]
b = b[b.marital == 1]
c = b.dropna(subset = ['satfin','hapmar', 'health','satjob'], how = 'any')
year_dummy = {2006:0, 2010:1}  # To mimic R's as.factor(year) function that converts 2006 to 0 and 2010 to 1
c["year_dum"] = c["year"].map(year_dummy.get)
lm1 = smf.ols(formula = "rhappy ~ year_dum", data = c).fit()
print lm1.summary()

# our complex model (slide 79)
lm2 = smf.ols(formula = "rhappy ~ year_dum + satfin", data = c).fit()
print lm2.summary()

# did I just cherry-pick (slide 82)
lm3 = smf.ols(formula = "rhappy ~ year_dum + hapmar", data = c).fit()
print lm3.summary()

lm4 = smf.ols(formula = "rhappy ~ year_dum + satjob", data = c).fit()
print lm4.summary()

lm5 = smf.ols(formula = "rhappy ~ year_dum + health", data = c).fit()
print lm5.summary()

### Do people whose dads have higher occupational prestige also have higher occupational prestige themselves? (slide 90)

# simple linear regression (slide 92)
lm_pres = smf.ols(formula = "prestg80 ~ papres80", data = d).fit()
print lm_pres.summary()

# multiple linear regression that takes education into account (slide 96)
lm_pres2 = smf.ols(formula = "prestg80 ~ papres80 + educ", data = d).fit()
print lm_pres2.summary()

#### Standardized Coefficients #### (slide 104)

### Do people coming from big families reproduce big families? or the opposite? (slide 108)

# simple linear regression (slide 109)
GSS_2010 = d[d.year == 2010]
GSS_2010_nonNAage = GSS_2010.dropna(subset = ["age"])
lm_family = smf.ols(formula = "childs ~ sibs", data = GSS_2010_nonNAage).fit()
print lm_family.summary()

# multiple regression that take age into account (slide 112)
lm_family2 = smf.ols(formula = "childs ~ sibs + age", data = GSS_2010_nonNAage).fit()
print lm_family2.summary()

## Whether siblings or age has a bigger effect on the number of children a person has?  (slide 114)
def stdCoef(fit):
    x = fit.model.data      # Access the original dataset
    sd = x.frame[x.xnames[1:]].std()   # Calculate the standard deviations of "sibs" and "age"
    sd_intercept = x.frame[x.ynames].std()  # Compute the standard deviation of the intercept
    coefficients = fit.params[1:]
    std_coefs = coefficients * (sd / sd_intercept)
    print "{0}".format("Standardized coefficients are: ")
    return std_coefs

stdCoef(lm_family2)

# create dummy variable for male (slide 121)
GSS_2010["male"] = pd.get_dummies(GSS_2010["sex"])[1]
GSS_2010_nonNAage = GSS_2010.dropna(subset = ["age"])

# multiple regression including the dummy for male 
lm_family3 = smf.ols(formula = "childs ~ sibs + age + male", data = GSS_2010_nonNAage).fit()
stdCoef(lm_family3)

### Which US regions has the lowest average age where people had their first baby  (slide 126)

# treatment (dummy) coding  (slide 128)
lm = smf.ols(formula = "agekdbrn ~ C(reg16, Treatment)", data = GSS_2010).fit()
print lm.summary()

# adding labels (slide 129)
GSS_2010["reg16_num"] = 1
pd.pivot_table(GSS_2010, index = ["reg16"], values = ["reg16_num"], aggfunc = np.sum, fill_value = 0)

GSS_2010["reg16_category"] = pd.Categorical(GSS_2010["reg16"], categories = range(0, 10), ordered = True)
GSS_2010["reg16_fact"] = GSS_2010.reg16_category.cat.rename_categories(["Foreign", "NewEngland", "MiddleAtlantic", "E.Nor.Central", "W.Nor.Central", "SouthAtlantic", "E.Sou.Central", "W.Sou.Central", "Mountain", "Pacific"]).values
pd.pivot_table(GSS_2010, index = ["reg16_fact"], values = ["reg16_num"], aggfunc = np.sum, fill_value = 0)

# change the reference (slide 131)  
lm = smf.ols(formula = "agekdbrn ~ C(reg16, Treatment(9))", data = GSS_2010).fit()  # we select #9 as reference, which is "Pacific"
print lm.summary()



























