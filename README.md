# PyMuMIn

This imitates the MuMIn package for R on Python

More specifically, this will imitate the dredge function of the package

The main goal is to find the correlation between DV and IV, controlling for the rest of the DVs

How to use - 
After importing it, you can call the function by -

MuMIn(x,y,dataframe)
x - list of strings only. the strings are essentially column header names. Do not worry about the format of the string. It will reformat before parsing it on smf.ols

y - takes in a string

dataframe - a valid pd dataframe

Other things that need to be done

1) To be able to add to specify if you should include the baseline category, or if to switch the baseline categories. this could be a dictionary
