#!/usr/bin/env python
# coding: utf-8

# In[19]:


import pandas as pd
import numpy as np


# In[20]:


np.random.seed(1256)


# In[24]:


def ballot_generator(participants,max_budget,n_projects,cost_per_project):
    ballot = [] 
    for i in range(participants):
        votes = []
        budget_remaining  = max_budget
        while budget_remaining >= min(cost_per_project):
            choice = np.random.choice(range(n_projects))
            votes.append(choice)
            budget_remaining -= cost_per_project[choice]
        s = set(votes)
        temp3 = [x for x in range(n_projects) if x not in s]
        for j in temp3:
            votes.append(j)
        ballot.append(votes)
    return ballot,max_budget,cost_per_project


# In[25]:


participants = 5000
max_budget = 1000000 #one million
n_projects = 10
cost_per_project = [150000,200000,250000,500000,135000,60000,350000,400000,225000,125000]


# In[26]:


ballot,max_budget,cost_per_project = ballot_generator(participants,max_budget,n_projects,cost_per_project)    


# In[ ]:





# In[ ]:





# In[ ]:




