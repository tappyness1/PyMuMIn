""" 
This code imitates the MuMIn package for R
More specifically, this will imitate the dredge function of the package
The main goal is to find the correlation between DV and IV, controlling for the rest of the DVs
"""

"""
Other things that need to be done
1) To be able to add to specify if you should include the baseline category, or if to switch the baseline categories. this could be a dictionary 
2) 
"""
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import random
import math

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

""" 
The below function returns a dictionary. The length of the dictionary is (2**N) - 1
The key is the serial number, the value is a model. 

arg1 is a list
arg2 is a string
arg3 is the df that you will be pulling the data from.
    
"""

def MuMIn(fulllist, IV, dataframe):
    

    varlist = fulllist
    Yvar = IV
    
    #drop all na rows from all the above specified variables
    sub1 = dataframe[varlist].dropna()
    
    YVarcleaned = ''.join(e for e in Yvar if e.isalnum())
    if str(sub1[Yvar].dtype) == "category" or str(sub1[Yvar].dtype) == "object":
        Yvarcleaned = 'C(' + Yvarcleaned + ')'
    else: 
        pass
    
    # convert all the vars to alphanumeric only so that smf.ols can read them
    # while it is possible to have smf.ols read them as is, you need to put in quite a 
    # number of string wrappers to read properly. We should avoid that.
    
    for i in varlist:
        # l = i.replace(" ", "_")
        l = ''.join(e for e in i if e.isalnum())
        print (l)
        if l == i:
            pass
        else: 
            sub1[l] = sub1[i]
            print(sub1[l].head(1))
            sub1 = sub1.drop([i], axis = 1)
    
    # smf.ols does not read categorical variables as is. need to convert them to 
    # readable format before parsing them to smf.ols 
    
    Xvar  = sub1.columns.tolist()
    Xvar1 = []
    for i in Xvar:
        if str(sub1[i].dtype) == "category" or str(sub1[i].dtype) == "object":
            Xvar1.append('C(' + i + ')')
        else: 
            Xvar1.append(i)
    Xvar1.remove(YVarcleaned)
    Xvar = Xvar1
    
    # build a list of lists of vars to use (basically all the possible models)
    # this uses the combination calculator 
    # it is similar to stepwise regression, but the goal is to know all the models
    # and not just select one good model.
    
    modellist = []
    
    for i in range(1, len(Xvar)+ 1):
        possiblecombis = nCr(len(Xvar), i)
        storelist = []
        while len(storelist) < possiblecombis:
            randvars = random.sample(set(Xvar), i)
            if randvars in storelist:
                pass
            else: 
                storelist.append(randvars)
                modellist.append(randvars)
    
    print (len(modellist))
    from sklearn.linear_model import LinearRegression
    
    modelsdict = {}
    
    essen = 1
    
    for listi in modellist:
        xvarstring = ' + '.join(str(elem) for elem in listi)
        fullstatement = YVarcleaned + ' ~ ' + xvarstring
        results = smf.ols(formula = fullstatement, data = sub1).fit()
        # modelsdict[' '.join(listi)] = results
        sn = "SN " + str(essen)
        modelsdict[sn] = results
        essen += 1
        
    # print ("Results :")
    # for key in modelsdict:
    #     print (key + ": " +  str(modelsdict[key]))
        
    return modelsdict