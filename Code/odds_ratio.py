#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#below code for mature dogs file, process is identical for other strata files


# In[1]:


import pandas as pd 
import numpy as np
import scipy.stats as stats
from scipy.stats import rankdata


# In[115]:


df = pd.read_csv("/Users/atmal/Downloads/matureDogs")
df = pd.DataFrame(df)


# In[116]:


#get index of final disease column
df.columns.get_loc("hs_cancer_types_unknown") 


# In[117]:


matureDogs=[]
maturepVals=[]
matureOdds=[]

# 7 is index of firstt disease colummn
for i in range(7,260):
  for j in range(7,260):
    if(i!=j):
      #make contingency table
      table=pd.crosstab(index=df.iloc[:,i],columns=df.iloc[:,j],margins=True) 
      #need 2x2 table so drop All column and row
      table=table.drop('All',axis=1)
      table=table.drop('All',axis=0)
      #calculate odds ratio and pvalue
      oddsratio, pvalue = stats.fisher_exact(table)
      #create columns for disease labels, pvals, odds
      matureDogs.append((str(df.columns[i])+"vs"+str(df.columns[j])))
      maturepVals.append(pvalue)
      matureOdds.append(oddsratio)
#convert to arrays
matureDogs=np.array((matureDogs))
matureDogspVals=np.array((maturepVals))
matureDogsOdds=np.array((matureOdds))

#concatenate arrays to matrix
mature=np.column_stack((matureDogs,maturepVals,matureOdds))

#export as csv
pd.DataFrame(mature).to_csv("/Users/atmal/Desktop/young.csv")


# In[118]:


#load csv and define individual columns
df = pd.read_csv("/Users/atmal/Desktop/young.csv")
pvals=df.iloc[:,2]
dogs=df.iloc[:,1]
odds=df.iloc[:,3]
pvals


# In[119]:


#apply Benjamini-Hochberg correction
ranked_p_values = rankdata(pvals)
padj = pvals * len(pvals) / ranked_p_values
padj[padj > 1] = 1


# In[121]:


#new matrix with adjust pvals
matureAdj = np.column_stack((dogs,padj,odds))


# In[123]:


#sort by odds and pvals conditions
newMatureO2=[]
for i in range(len(newMatureAdj)):
    if(float(newMatureAdj[i][1])<0.01 and float(newMatureAdj[i][2])>2):
        newMatureO2.append(newMatureAdj[i])


# In[124]:


#save to new csv
pd.DataFrame(newMatureO2).to_csv("/Users/atmal/Desktop/matureAdjO2.csv")


# In[ ]:




