# Data Analysis for the Social Sciences Presentation 5
# Author: Xu (Conan) Huang
# Topics: Log transformations, multiple regression, and interactions

from __future__ import division
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import os
import matplotlib.pyplot as plt

#### Log Transformation ####

# distribution on realrinc (slide 5)
os.chdir("C:/GSS")
d = pd.read_csv("GSS_Cum.csv")
sub = d[d["year"] == 2006]

sub["realrinc"].plot(kind = 'hist')    # histogram with raw counts
plt.title("Histogram of d['realrinc']")

sub.hist('realrinc', bins = 8, normed = True)   # "normed = True" argument gives you frequency rather than raw counts
plt.title("Histogram of d['realrinc']")

# distribution of ln.realrinc (slide 6)
sub["ln_realrinc"] = np.log(sub["realrinc"])
sub["ln_realrinc"].plot(kind = 'hist') 
plt.title("Histogram of log(d['realrinc'])")

# a log-log model (slide 8)
sub["ln_hrs1"] = np.log(sub["hrs1"])
sub["ln_realrinc"] = np.log(sub["realrinc"])
lm1 = smf.ols(formula = "ln_realrinc ~ ln_hrs1 + C(sex)", data = sub).fit()
print lm1.summary()

# a level-log model (slide 10)
sub["ln_wordsum"] = np.log(sub["wordsum"])
sub["working"] = sub["wrkstat"].apply(lambda e: 1 if e < 3 else 0)
sub["ln_wordsum"] = sub["ln_wordsum"].map(lambda x: np.nan if x == -inf else x)

lm2 = smf.ols(formula = "tvhours ~ ln_wordsum + working", data = sub).fit()
print lm2.summary()

# Another log-log model ( slide 12)
os.chdir("C:/Users/Conan/Desktop")
b = pd.read_csv("movies-bechdel.csv")

b["tg13"] = b["domgross_2013$"] + b["intgross_2013$"]
b["tot_gross_13_mil"] = b["tg13"] / (1000000)
b["budget_13_mil"] = b["budget_2013$"] / (1000000)

b["ln_bud"] = np.log(b["budget_13_mil"])
b["ln_tot"] = np.log(b["tot_gross_13_mil"])

lm1 = smf.ols(formula = "ln_tot ~ binary", data = b).fit()
print lm1.summary()

lm2 = smf.ols(formula = "ln_tot ~ binary + ln_bud", data = b).fit()
print lm2.summary()

lm3 = smf.ols(formula = "tot_gross_13_mil ~ binary + budget_13_mil", data = b).fit()
print lm3.summary()

#### Multiple regression ####

### What are the effects of educational attainment and being a man on occupational prestige?

# some recodes to create the DataFrame that contains 9 observations from year 2006 and 2008
sub_2008 = d[d['year'] == 2008]
sub_2008_new = sub_2008[sub_2008['id'].isin([564, 895, 1537])]
sub_2006_new = sub[sub['id'].isin([605, 1650, 3014, 3076, 3352, 3726])]
obs_9 = pd.concat([sub_2006_new, sub_2008_new])

# correlations (slide 19) 
sex_dummy = {1:0, 2:1}
obs_9['male'] = obs_9['sex'].map(sex_dummy.get)
obs_9_sub = obs_9[["prestg80","educ","male"]]
obs_9_sub.corr(method = 'pearson')

# multiple regression (slide 22)
lm = smf.ols(formula = "prestg80 ~ educ + male", data = obs_9).fit()
print lm.summary()

# regress educ on malenesss (slide 23)
lm_male = smf.ols(formula = "educ ~ male", data = obs_9).fit()
print lm_male.summary()

# residuals  (slide 28)
lm.resid

#### Interactions ####

### At higher levels of education, are the differences ampliefied or minimized between men and women on income? (slide 44)

# recodes (slide 45)
sub_new = sub[["realrinc", "educ", "sex"]]
sub_new["female"] = sub_new["sex"] == 2
sub_new = sub_new.dropna(subset = ["realrinc", "educ"])

# multiple regression (slide 46)
lm_income = smf.ols(formula = "realrinc ~ educ + female", data = sub_new).fit()
print lm_income.summary() 
sub_new["fitted"] = lm_income.predict()

# graph (slide 49)
educ_linspace = np.linspace(sub_new.educ.min(), sub_new.educ.max(), 100)

plt.plot(sub_new["educ"], lm_income.params[0] + lm_income.params[1] * 1 + lm_income.params[2] * sub_new["educ"], 'r', label = 'female', alpha = 0.9)
plt.plot(sub_new["educ"], lm_income.params[0] + lm_income.params[1] * 0 + lm_income.params[2] * sub_new["educ"], 'b', label = 'male', alpha = 0.9)
plt.title("Men vs women on income")
plt.xlabel("educ")
plt.ylabel("fitted")

# simple regression for men (slide 50)
lm_males = smf.ols(formula = "realrinc ~ educ", data = sub_new, subset = sub_new.female == 0).fit()
print lm_males.summary()

# simple regression for women (slide 51)
lm_females = smf.ols(formula = "realrinc ~ educ", data = sub_new, subset = sub_new.female == 1).fit()
print lm_females.summary()

# the interaction model I (slide 52)
# Note: the * in the formula means that we want the interaction term in addition to each term separately
# use : instead if you want to include the interaction term only 
lm_income2 = smf.ols(formula = "realrinc ~ educ * female", data = sub_new).fit()
print lm_income2.summary()

lm_income_2 = smf.ols(formula = "realrinc ~ educ : female", data = sub_new).fit()
print lm_income_2.summary()

# graph (slide 55)
plt.plot(sub_new["educ"], lm_income2.params[0] + lm_income2.params[1] * 1 + lm_income2.params[2] * sub_new["educ"] + lm_income2.params[3] * 1 * sub_new["educ"], 'r', label = 'female', alpha = 0.9)
plt.plot(sub_new["educ"], lm_income2.params[0] + lm_income2.params[1] * 0 + lm_income2.params[2] * sub_new["educ"] + lm_income2.params[3] * 0 * sub_new["educ"], 'b', label = 'male', alpha = 0.9)
plt.title("Men vs women on income with interaction")
plt.xlabel("educ")
plt.ylabel("realrinc")

### Do well-off kids suffer educationally the same amount for each additional sibling,
### as do non-well-off kids?

# simple multiple regression (slide 60)
sub_kids = sub[["educ", "sibs", "madeg", "family16", "age"]]
sub_kids["maBA"] = sub_kids['madeg'].isin([3,4])

lm_maBA = smf.ols(formula = 'educ ~ sibs + maBA', data = sub_kids).fit()
print lm_maBA.summary()

# simple regression for kids of <BA moms (slide 63)
lm_maBA0 = smf.ols(formula = 'educ ~ sibs', data = sub_kids, subset = sub_kids.maBA == 0).fit()
print lm_maBA0.summary()

# simple regression for kids of BA+ moms (slide 64)
lm_maBA1 = smf.ols(formula = 'educ ~ sibs', data = sub_kids, subset = sub_kids.maBA == 1).fit()
print lm_maBA1.summary()

# interaction model I (slide 65)
lm_maBA_Inter = smf.ols(formula = 'educ ~ sibs * maBA', data = sub_kids).fit()
print lm_maBA_Inter.summary()

# graph (slide 68)
plt.axis([0, 35, 0, 18])
plt.plot(sub_kids["sibs"], lm_maBA_Inter.params[0] + lm_maBA_Inter.params[1] * 0 + lm_maBA_Inter.params[2] * sub_kids["sibs"] + lm_maBA_Inter.params[3] * 0 * sub_kids["sibs"], 'cyan', label = '<BA', alpha = 0.9)
plt.plot(sub_kids["sibs"], lm_maBA_Inter.params[0] + lm_maBA_Inter.params[1] * 1 + lm_maBA_Inter.params[2] * sub_kids["sibs"] + lm_maBA_Inter.params[3] * 1 * sub_kids["sibs"], 'purple', label = 'BA+', alpha = 0.9)
plt.title("Kids of BA+ moms vs not with interaction")
plt.xlabel("sibs")
plt.ylabel("educ")

# multiple linear regression with other variables (slide 70)
sub_kids["twobio"] = sub_kids["family16"] == 1
lm_maBA_twobio = smf.ols("educ ~ sibs * maBA + age + twobio", data = sub_kids).fit()
print lm_maBA_twobio.summary()

### Does education alter fundamentalists opinion on evolution ? (slide 74)

# recodes
sub_evo = sub[["educ", "fund", "evolved", "family16", "age"]]
fund_dummy = {1:1, 2:0, 3:0}
sub_evo["fundamentalist"] = sub_evo["fund"].map(fund_dummy.get)
evolved_dummy = {1:1, 2:0}
sub_evo["evolution"] = sub_evo["evolved"].map(evolved_dummy.get)

# simple multiple regression (slide 76)
lm_evo = smf.ols(formula = 'evolution ~ fundamentalist + educ', data = sub_evo).fit()
print lm_evo.summary()

# interaction model I (slide 78)
lm_evo_Inter = smf.ols(formula = 'evolution ~ educ * fundamentalist', data = sub_evo).fit()
print lm_evo_Inter.summary()

# graph (slide 81)
plt.axis([0, 20, 0, 0.9])
plt.plot(sub_evo["educ"], lm_evo_Inter.params[0] + lm_evo_Inter.params[1] * sub_evo["educ"] + lm_evo_Inter.params[2] * 0 + lm_evo_Inter.params[3] * 0 * sub_evo["educ"], 'blue', label = 'Not Fundamentalist', alpha = 0.9)
plt.plot(sub_evo["educ"], lm_evo_Inter.params[0] + lm_evo_Inter.params[1] * sub_evo["educ"] + lm_evo_Inter.params[2] * 1 + lm_evo_Inter.params[3] * 1 * sub_evo["educ"], 'red', label = 'Fundamentalist', alpha = 0.9)
plt.title("Fundamentalists vs. non-fundamentalists with interactions")
plt.xlabel("educ")
plt.ylabel("evolution")

# find the mean (slide 83)
sub_evo["educ"].mean()

# recode (slide 84)
sub_evo["center_educ"] = sub_evo["educ"] - sub_evo["educ"].mean()

sub_evo["center_educ"].describe().map(lambda x: round(x, 4))

# interaction model I modified (slide 85)
lm_evo_Inter2 = smf.ols(formula = 'evolution ~ center_educ * fundamentalist', data = sub_evo).fit()
print lm_evo_Inter2.summary()

### Remember Wordsum & Marriage (slide 91)

# recodes (slide 92)
sub_word = sub[["marital", "wordsum", "educ", "speduc"]]
sub_word["married"] = sub_word["marital"] == 1

# multiple regression (slide 93)
lm_wordsum = smf.ols(formula = 'wordsum ~ married + educ', data = sub_word).fit()
print lm_wordsum.summary()

# the interaction model I (slide 95)
lm_wordsum2 = smf.ols(formula = 'wordsum ~ married * educ', data = sub_word).fit()
print lm_wordsum2.summary()

# graph (slide 97)
plt.axis([0, 20, 0, 9])
plt.plot(sub_word["educ"], lm_wordsum2.params[0] + lm_wordsum2.params[1] * 0 + lm_wordsum2.params[2] * sub_word["educ"] + lm_wordsum2.params[3] * 0 * sub_word["educ"], 'green', label = 'Unmarried', alpha = 0.9)
plt.plot(sub_word["educ"], lm_wordsum2.params[0] + lm_wordsum2.params[1] * 1 + lm_wordsum2.params[2] * sub_word["educ"] + lm_wordsum2.params[3] * 1 * sub_word["educ"], 'purple', label = 'Married', alpha = 0.9)
plt.title("Married vs unmarried with interactions")
plt.xlabel("educ")
plt.ylabel("wordsum")

# the interaction model II (slide 100)
lm_speduc = smf.ols(formula = 'wordsum ~ educ * speduc', data = sub_word).fit()
print lm_speduc.summary()

# graph (slide 107)
plt.axis([0, 20, 0, 9])
plt.plot(sub_word["educ"], lm_speduc.params[0] + lm_speduc.params[1] * sub_word["educ"] + lm_speduc.params[2] * 0 + lm_speduc.params[3] * 0 * sub_word["educ"], 'green', label = 'SpEduc = 0', alpha = 0.9)
plt.plot(sub_word["educ"], lm_speduc.params[0] + lm_speduc.params[1] * sub_word["educ"] + lm_speduc.params[2] * 10 + lm_speduc.params[3] * 10 * sub_word["educ"], 'purple', label = 'SpEduc = 10', alpha = 0.9)
plt.plot(sub_word["educ"], lm_speduc.params[0] + lm_speduc.params[1] * sub_word["educ"] + lm_speduc.params[2] * 20 + lm_speduc.params[3] * 20 * sub_word["educ"], 'blue', label = 'SpEduc = 20', alpha = 0.9)
plt.title("Varying spouse's education level with interactions")
plt.xlabel("educ")
plt.ylabel("wordsum")

### Does someone become healthier with more education and increased religious attendance? (slide 110)
health_dummy = {1:4, 2:3, 3:2, 4:1}
d["rhealth"] = d["health"].map(health_dummy.get)

# multiple regression model (slide 111)
lm_health = smf.ols(formula = 'rhealth ~ educ + attend + age', data = d).fit()
print lm_health.summary()

# interaction model (slide 112)
lm_health_Inter = smf.ols(formula = 'rhealth ~ educ * attend + age', data = d).fit()
print lm_health_Inter.summary()





