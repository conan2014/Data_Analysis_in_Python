# Data Analysis for the Social Sciences Presentation 10
# Author: Xu (Conan) Huang
# Topics: Scales, Principal Component Analysis, & Factor Analysis
# Written using Python 2.7.6 in Enthought Canopy in Windows 7 

from __future__ import division
import pandas as pd 
import numpy as np
import statsmodels.formula.api as smf
import os

### Scales ###
os.chdir("C:/GSS")
GSS = pd.read_csv("GSS_Cum.csv")
d = GSS[GSS.year == 2010]

var = ['reborn', 'relexp', 'attend', 'fund', 'reliten', 'relneg', 'relpersn','pray','punsin']
sub = d[var] 

# Get correlations between all variables
sub.corr(method = 'pearson')

# Cronbach's alpha (Currently Statsmodels package cannot support this)

# Multiple regression using all variables
sub['polviews'] = d['polviews']  # variable 'polviews' is added as the last column in DataFrame sub
lm_polviews = smf.ols(formula = 'polviews ~ reborn + relexp + attend + fund + reliten + relneg + relpersn + pray + punsin', data = sub).fit()
print lm_polviews.summary()

def stdCoef(fit):
    x = fit.model.data      # Access the original dataset
    sd = x.frame[x.xnames[1:]].std()   # Calculate the standard deviations of "sibs" and "age"
    sd_dv = x.frame[x.ynames].std()  # Compute the standard deviation of the dependent variable "childs"
    coefficients = fit.params[1:]
    std_coefs = coefficients * (sd / sd_dv)
    print ("Standardized coefficients are: ")
    return std_coefs

stdCoef(lm_polviews) # standardized coeffcients

# Variance Inflation Factor

def vif(fit): 
    from statsmodels.stats.outliers_influence import variance_inflation_factor as smvif
    from patsy import dmatrix # used to construct design matrix since variance_inflation_factor function only accepts design matrix
    x = fit.model.data
    dicty = x.frame.to_dict('list') # Convert DataFrame to dictionary. Dict-like {column -> [values]}
    formula_like = '+'.join(x.xnames[1:])  # produce formula_like such as "a + b"
    design_matrix = dmatrix(formula_like, dicty)
    for item in range(1, len(x.xnames)): # Here range starts with 1 instead of 0 because we want to exclude the intercept term in our final result
        print x.xnames[item] + ': ' + str(smvif(design_matrix, item))

vif(lm_polviews)

## Make Scale

# reverse code some variables
keys = [-1,-1, 1,-1,-1, 1,-1,-1,-1, 1]

def reverse_code(keys, items):
    assert len(keys) == len(items.columns), "Please provide keys for each columns"
    for i in range(len(keys)):
        if keys[i] == -1:
            items.ix[:,i] = items.ix[:,i].max() - items.ix[:,i] + 1
    return items

subs = reverse_code(keys = keys, items = sub)

# create scale by standardizing and taking row mean
from sklearn import preprocessing

# impute missing values. The default method is to fill missing value with
# the mean of its respective column
subs_trunc = subs.ix[:, :len(subs.columns)-1] # exclude the last column 'polviews'
impute = preprocessing.Imputer()
subs_trunc_prime = impute.fit_transform(subs_trunc)

# scale the imputed DataFrame
my_scaler = preprocessing.StandardScaler()
subs_prime_scale = my_scaler.fit_transform(subs_trunc_prime)
subs_temp = pd.DataFrame(subs_prime_scale) # convert numpy ndarray into DataFrame
subs_temp.columns = subs.columns[:len(subs.columns)-1]
subs['religion'] = subs_temp.mean(axis = 1)

lm_religion = smf.ols(formula = 'polviews ~ religion', data = subs).fit()
print lm_religion.summary()
stdCoef(lm_religion)

## Principal Component Analysis (PCA) & Factor Analysis

GSS = pd.read_csv("GSS_Cum.csv")
sub = GSS.ix[:,'confinan':'conarmy'] 

# Reverse code all of the variables
keys = np.repeat(-1, len(sub_pca.columns)) # array of -1s with length equal to the number of columns in sub_pca
sub_pca = reverse_code(keys = keys, items = sub)

# impute missing value in DataFrame sub_pca
impute = preprocessing.Imputer()
sub_pca_imputed = impute.fit_transform(sub_pca)

# PCA
from sklearn import decomposition

pca = decomposition.PCA()
sub_pca_prime = pca.fit_transform(sub_pca_imputed) 

pca.n_components_  # the estimated number of components
pca.components_  # principal component loadings
pca.explained_variance_ratio_ # percentage of variance explained by each principal components
pca.explained_variance_ratio_.cumsum()  # cumulative sum of percentage of variance explained


# Factor Analysis
GSS = pd.read_csv("GSS_Cum.csv")
sub = GSS.ix[:,'confinan':'conarmy']

# impute missing value in DataFrame sub
from sklearn import preprocessing
impute = preprocessing.Imputer()
sub_imputed = impute.fit_transform(sub)

# use FactorAnalysis package 
from sklearn.decomposition import FactorAnalysis
fa = FactorAnalysis(n_components = 5, max_iter = 100) #Here we set dimensionality of latent space to be 5 and maximum number of iterations to be 100
sub_fa = fa.fit_transform(sub_imputed)

fa.components_  # factor loadings
fa.loglike_   # the log likelihood at each iteration
fa.n_iter_   # Number of iterations run



