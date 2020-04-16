#!/usr/bin/env python
# coding: utf-8

# In[42]:


import pandas as pd
import numpy as np


# In[43]:


def ballot_generator(participants,max_budget,n_projects,cost_per_project):
    ballot = [] 
    for i in range(participants):
        votes = []
        budget_remaining  = max_budget
        while budget_remaining >= min(cost_per_project):
            choice = np.random.choice(range(n_projects))
            votes.append(choice)
            budget_remaining -= cost_per_project[choice]
        a = [0 for i in range(n_projects)]
        for i in votes:
            a[i] = 1
        
        ballot.append(a)
    return ballot,max_budget,cost_per_project


# In[44]:


def generator_multiple():
    np.random.seed(1256)
    participants = 5000
    max_budget = 1000000 #one million
    n_projects = 10
    cost_per_project = [150000,200000,250000,500000,135000,60000,350000,400000,225000,125000]
    for i in range(10):
        
        ballot,a,b = ballot_generator(participants,max_budget,n_projects,cost_per_project)
        np.save('ballot'+str(i),ballot)
    


# In[45]:


generator_multiple()


# In[ ]:




