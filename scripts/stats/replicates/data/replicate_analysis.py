#!/usr/bin/python

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_rel

def ts_independent(vec_1, vec_2):
    var1 = np.var(vec_1)
    var2 = np.var(vec_2)
    vars = [var1, var2]
    evar = False
    if max(vars) / min(vars) <= 4:
        evar = True

    stat, p = stats.ttest_ind(a = vec_1, b = vec_2, equal_var= evar)
    return {"t-stat":round(stat, 4), "p-value":round(p, 4)} 

def get_corr(vec_1, vec_2):

    coeff, pval = stats.pearsonr(vec_1, vec_2)

    return {"corr-coefficient": round(coeff, 4), "p-value": round(pval, 4)}

def run_stats(data, label, orientation, paired = False):
    a_var = label + "_2"
    b_var = label + "_3"

    A = data[a_var].to_list()
    B = data[b_var].to_list()
    
    t = ts_independent(A,B)
    p = get_corr(A,B)
    
    if paired == True:
    	t = ttest_rel(A, B)
    	
    data = {'Two-Samp_T-Test': t, 'Pearson_Correlation':p}
    dataframe = pd.DataFrame(data)
    print(dataframe)
    dataframe.to_csv("./results/" + orientation + "/stats_" + label + ".csv")
    return data, A, B

def plot_stats(data_dict, orientation, label, vec1, vec2):

    plt.style.use('ggplot')
    plt.rcParams["figure.figsize"] = (10, 10)
    plt.hist(vec1, bins = 50, label = "instance 2", alpha = 0.75)
    plt.hist(vec2, bins = 50, label = "instance 3", alpha = 0.5)
    plt.plot([], [], ' ', label = "T-Test p-val:\n" + str(round(data['Two-Samp_T-Test']["p-value"], 3)))
    plt.plot([], [], ' ', label = "Pearson coeff:\n" + str(round(data['Pearson_Correlation']["corr-coefficient"], 3)))
    plt.legend()
    plt.title(label)
    plt.savefig("./figures/" + orientation + "_" + col + ".png")

def pairplot(data, orientation, feature_list = ['quad_1_av', 'quad_2_av', 'quad_3_av', 'average']):
    sns.set_theme(style = 'dark')
    sns_plot = sns.pairplot(data, hue="instance", palette = "dark", vars = feature_list, diag_kind="hist",height = 5)
    sns_plot.figure.savefig("./figures/" + orientation + "_joint_space_pairplot.png")