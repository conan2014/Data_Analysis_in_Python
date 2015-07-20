# Data Analysis for the Social Sciences Presentation 8
# Author: Xu (Conan) Huang
# Topics: Logit regression, ordinal logistic regression, and multinomial logistic regression

from __future__ import division
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.formula.api import rlm
import statsmodels.api as sm
from statsmodels.regression.quantile_regression import QuantReg
from tabulate import tabulate
import math

import os
import scipy
import scipy.stats as stat


#### Logit regression assumptions ####

### What predicts whether someone will say it's okay for someone to commit suicide (slide 14)
### if they become bankrupt 

# simple logistic regression (slide 22)
os.chdir("C:/GSS")
d = pd.read_csv("GSS_Cum.csv")
sub = d[d.year == 2006]
suicide_dummy = {1:1, 2:0}
sub["suicidebank"] = sub["suicide2"].map(suicide_dummy.get)

import patsy # use Patsy package to easily create the target vector (y) and design matrix (x)
f = 'suicidebank ~ age + educ + C(marital) + attend'
y, x = patsy.dmatrices(f, sub, return_type = 'dataframe')

logit_suicide = sm.Logit(y, x).fit()
print logit_suicide.summary()

# Wald Test
logit_suicide.wald_test(["age", "educ"])

# Akaike Information Criterion (slide 23)
logit_suicide.aic   

# manually calculate AIC
AIC = 2 * len(logit_suicide.params) - 2 * logit_suicide.llf  # llf is the log likehood of the fitted model
AIC

# pseudo R squared
logit_suicide.prsquared

# manually calculate pseudo R squared
pr_squared = 1 - logit_suicide.llf/logit_suicide.llnull
pr_squared

# log-likelihood from the fitted model and from the intercept-only model
logit_suicide.llf
logit_suicide.llnull

#### Ordinal logit regression #### (slide 25)

# Table function
import collections
def Table(data, variable, labels = None, digits = 2):   # variable accepts arguments enclosed with single or double quotes, labels accepts a list
    tab = pd.DataFrame({'Freq.':[], 'Percent': [], 'Percent.Cum': []})
    count = {}
    for value, value_table in data.groupby(variable):   # use "groupby" to split-apply-combine
        #array = value_table[variable].values
        count[value] = len(value_table[variable].dropna())
    count_ordered = collections.OrderedDict(sorted(count.items()))
    total = sum(count_ordered.values())
    tab['Freq.'] = count_ordered.values()
    tab['Percent'] = np.round(count_ordered.values()/total * 100 , digits) # the default is round up to 3 decimal places
    tab['Percent.Cum'] = tab['Percent'].cumsum()
    if labels == None:
        tab.index = count_ordered.keys() 
    else:
        tab.index = labels
    return tab

### What predicts if you want to spend more government money on child care? (slide 27)

var = ["natchld", "marital", "realinc", "age", "polviews", "childs"]
sub_child = sub[var]
sub_child["realinc_log"] = sub_child["realinc"].map(lambda x: math.log(x))

marital_dummy = {1:1, 2:0, 3:0, 4:0, 5:0}
sub_child["married"] = sub_child["marital"].map(marital_dummy)
Table(sub_child, "natchld")

f = 'natchld_temp ~ childs + age + married + realinc_log + polviews'
y, x = patsy.dmatrices(f, sub_child, return_type = 'dataframe')
y = np.asarray(y)
X = np.asarray(x)

ordinal_logistic_fit(X, y, verbose=True, solver='TNC')  # error message 

sub_child["natchld_temp"] = pd.Categorical(sub_child.natchld, categories = [1, 2, 3], ordered = True) # 1 < 2 < 3 as ordered = True
sub_child['natchld_float'] = sub_child['natchld_temp'].astype(float) 
sub_child['childcare'] = np.asarray(sub_child["natchld_temp"].cat.rename_categories(["too little", "about right", "too much"]).values) # 'too little' represents '1' and so on
Table(sub_child, "childcare")

# collapse the categories into 'too much' vs. 'about right' and 'too little' (slide 33)
sub_child["childcare_23"] = sub_child["childcare"].map(lambda x: 1 if x == "about right" or x == "too little" else 0 if x == "too much" else np.nan)
sub_child["childcare_3"] = sub_child["childcare"].map(lambda x: 1 if x == "too little" else 0 if x == "about right" or x == "too much" else np.nan)

# binary logit predicting log-odds of being in higher opinion category vs. believing we spent "too much" on child care (slide 34)
k = 'childcare_23 ~ childs + age + married + realinc_log + polviews'
y, x = patsy.dmatrices(k, sub_child, return_type = 'dataframe')
logit_23_vs_1 = sm.Logit(y, x).fit()
print logit_23_vs_1.summary()

from IPython.core.display import HTML   # or you can display a short summary 
def short_summary(est):
    return HTML(est.summary().tables[1].as_html())
short_summary(logit_23_vs_1)

# slide 36
p = 'childcare_3 ~ childs + age + married + realinc_log + polviews'
y, x = patsy.dmatrices(p, sub_child, return_type = 'dataframe')
logit_12_vs_3 = sm.Logit(y, x).fit()
print logit_12_vs_3.summary()

# (add in the result from ordinal logit regression!!!) comparing results  (slide 37)
coeff_table = pd.DataFrame({"Logit (2, 3, vs. 1)": logit_23_vs_1.params[1:]
, "Logit (1,2 vs. 3)": logit_12_vs_3.params[1:]} )
coeff_table

#### Multinomial logit regression #### (slide 42)

### (result appears different Multinomial logit regression (slide 46)
f = 'natchld_float ~ childs + age + married + realinc_log + polviews'
y, x = patsy.dmatrices(f, sub_child, return_type = 'dataframe')
multinom_child = sm.MNLogit(y, x).fit()
print (multinom_child.params) 
print multinom_child.summary

# need Z-stats, p-values, and relative risk ratios (slide 47)
pnorm = stat.norm.cdf
b = multinom_child.params
b
se = multinom_child.bse
p_vals = 2 * (1 - pnorm(abs(b/se)))
p_vals

np.exp(multinom_child.params[1:])  # Extract the relative risk ratios

### Which possible effects of global warming do you care about the most? (slide 53)
cols = ["caremost", "sex", "educ", "age", "polviews", "fund"]
subset = sub[cols]
subset.describe()

Table(subset, "caremost", labels = ["the extinction of the polar bears", "the rise in sea level", "the threat to the arctic seals", "the threat to the inuit way of life", "the melting of the northern ice cap"])



