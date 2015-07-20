# Data Analysis for the Social Sciences Presentation 6
# Author: Xu (Conan) Huang
# Topics: Quadratics, F-tests, and adjusted R-square

from __future__ import division
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm
import os
import matplotlib.pyplot as plt

#### Quadratic terms ####
### Who gets angry the most 

# simple linear regression (slide 7)
os.chdir("C:/GSS")
d = pd.read_csv("GSS_Cum.csv")
sub = d[["angry", "sei"]]

lm_angry = smf.ols(formula = "angry ~ sei", data = sub).fit()
print lm_angry.summary()

# 2nd order polynomial regression  (slide 8)
model_angry2 = smf.ols(formula = 'angry ~ sei + I(sei ** 2.0)', data = sub)
lm_angry2 = model_angry2.fit()
print lm_angry2.summary()

# scatter plot (slide 13)
#X = pd.DataFrame({'sei':np.linspace(sub.sei.min(), sub.sei.max(), 100)})
X = np.linspace(sub.sei.min(), sub.sei.max(), 100)[:, np.newaxis]
plt.figure()
plt.plot(sub["sei"], sub["angry"], 'ro')
X_constant = sm.add_constant(X)

lm_angry2 = smf.ols(formula = 'angry ~ sei + I(sei ** 2.0) + I(sei ** 3.0)', data = sub).fit()
print lm_angry2.summary()

### Do Republicans go to religious services more often than Democrats (slide 22)

sub = d[["attend", "partyid"]]
sub_no7 = sub[sub["partyid"] < 7]

# simple linear regression  (slide 23)
lm_attend = smf.ols(formula = "attend ~ partyid", data = sub_no7).fit()
print lm_attend.summary()

## graph the raw data  (slide 24)

# one way is to use plot function
partyid_temp = {}
for party, party_table in sub_no7.groupby("partyid"):
    partyid_temp[party] = party_table['attend'].mean()
partyid_temp

s = pd.Series(partyid_temp)
my_color = 'bgcwymr'   # blue, green, cyan, white, yellow, magenta, red
pd.Series.plot(s, kind = "bar", color = my_color)

# another way is to use plotly package where you can edit the graph online
import plotly.plotly as py       
from plotly.graph_objs import *

data = Data([Bar( x = ["strong dem", "dem", "ind (dem)", "ind", "ind (rep)", "rep", "strong rep"], y = partyid_temp.values())])
plot_url = py.plot(data, filename = 'basic-bar') 

# curvilinear regression (slide 27)
lm_attend2 = smf.ols(formula = "attend ~ partyid + I(partyid ** 2)", data = sub_no7).fit()
print lm_attend2.summary()

# graph the curve  (slide 29)
X = pd.DataFrame({'partyid':np.linspace(sub_no7.partyid.min(), sub_no7.partyid.max(), 10)})
plt.figure()
plt.plot(X.partyid, lm_attend2.predict(X), 'b-')


#### F Tests ####
### Do trust levels vary by race? (slide 32)

# Recodes (slide 33)
sub = d[["trust", "race", "realinc", "educ", "region"]]
trust_dict = {1:3, 2:1, 3:2}
sub["new_trust"] = sub["trust"].map(trust_dict.get)
sub["black"] = sub["race"] == 2

# simple linear regression (slide 33)
sub_noNa = sub.dropna(subset = ["educ", "realinc", "region"])
lm_trust = smf.ols(formula = "new_trust ~ black", data = sub_noNa).fit()
print lm_trust.summary()

# the ANOVA test (slide 36)
import statsmodels.api as sm
print (sm.stats.anova_lm(lm_trust, typ = 1))

# add in more predictors (slide 40)
lm_trust2 = smf.ols(formula = "new_trust ~ black + educ + I(np.log(realinc)) + C(region) ", data = sub).fit()
print lm_trust2.summary()

# partial F-test (slide 44)
from statsmodels.stats.anova import anova_lm
table = anova_lm(lm_trust, lm_trust2)
table

#### OLS assumptions and diagnostics ####

# no perfect collinearity (slide 52)
GSS_2006 = d[d["year"] == 2006]
lm_age = smf.ols(formula = "tvhours ~ age + age", data = GSS_2006).fit()
print lm_age.summary()

# about heteroskedasticity (slide 57) 
lm_tv = smf.ols(formula = "tvhours ~ degree", data = GSS_2006).fit()
print lm_tv.summary()
lm_tv.pvalues

import statsmodels
statsmodels.stats.diagnostic.het_breushpagan(lm_tv)

# create side-by-side boxplot (slide 59)
GSS_2010_t = GSS_2010.dropna(subset = ["tvhours", "degree"])
e = lm_tv.resid    # extract residuals
dat = lm_tv.model.data
deg = dat.frame[dat.xnames[1]] # extract the observations of 'degree' used in fitting the model

def Series_boxplot(x, y, labels):
    new_dataframe = pd.concat([x, y], axis = 1)  # combine two Series into one DataFrame
    
    deg_temp = {}
    for degre, degre_group in new_dataframe.groupby(1):  # group Residuals by degree
        deg_temp[degre] = degre_group

    new_ndarray = []
    for i in range(len(deg_temp)):
        new_ndarray.append(np.asarray(deg_temp[i][0]))  # convert Series into numpy.ndarray and place all of them into a list

    new_removeNaN = []
    for array in new_ndarray:
        new_removeNaN.append(array[~np.isnan(array)]) # remove NaN values from each numpy.ndarray in the list
    
    plt.boxplot(new_removeNaN, labels = labels)

Series_boxplot(e, deg, labels = ["<HS","HS","JrCol","BA",">BA"])

# robust standard errors when we have heteroskedasticity (slide 64)
lm_robust = smf.ols(formula = "tvhours ~ degree", data = GSS_2006).fit(cov_type='HC0') # standard errors are heteroscedasticity robust (HC0)
print lm_robust.summary()


