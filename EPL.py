#!/usr/bin/env python
# coding: utf-8

# In[224]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[225]:


data=pd.read_csv('C:/Users/Toshiba/Downloads/all_match_results.csv')


# In[241]:


data['HomeTeamScore']=data['Result'].str[0].astype('int')
data['AwayTeamScore']=data['Result'].str[2:].astype('int')
data['TeamWon']=np.where((data['HomeTeamScore']>data['AwayTeamScore']) & (data['HomeTeamScore']!=data['AwayTeamScore']),
                         data['HomeTeam'],data['AwayTeam'])
data['TeamLost']=np.where((data['HomeTeamScore']>data['AwayTeamScore']) & (data['HomeTeamScore']!=data['AwayTeamScore']),
                         data['AwayTeam'],data['HomeTeam'])
most_team_won=data['TeamWon'].value_counts()
data['GoalDiff']=(data['HomeTeamScore']-data['AwayTeamScore']).abs()
data['WinningTeamGoalDiff']=data['GoalDiff']
data['LosingTeamGoalDiff']=data['GoalDiff']*-1
teamsData=pd.DataFrame(most_team_won)
teamsData.rename(columns={'TeamWon':'NumberOfWins'}, inplace = True)
g=sns.barplot(x=teamsData.index,y='NumberOfWins',data=teamsData)
g.set(xlabel='Premier League Teams',ylabel='Number Of Wins Of Each Team')
plt.xticks(rotation=80)

# plt.show()


# In[228]:


# teamsData['GoalDifference']=
data.head(45)


# In[232]:


data['Date']=data['Date'].astype('datetime64[ns]')
GDD=data.sort_values(by='Date').groupby('Date')['GoalDiff'].agg('sum')
GDD=pd.DataFrame(GDD)
data=data.merge(GDD,how='inner',on='Date',suffixes=('_Match','_Date'))


# In[156]:


data['Date']=data['Date'].dt.date
g2=sns.barplot(x='Date',y='GoalDiff_Date',data=data.sort_values(by='GoalDiff_Date',ascending=False).head(100))
plt.xticks(rotation=90)
plt.show()


# In[242]:


teamsData['Teams']=teamsData.index
teamsData['NOW']=teamsData['NumberOfWins']
teamsData['NumberOfWins']=0
teamsData.rename(columns={'NumberOfWins':'Goal Difference'},inplace=True)
teamsData.reset_index(inplace=True)
print(teamsData)


# In[272]:


for index_teams,rows_teams in teamsData.iterrows():
    val2=0
    for index_data,rows_data in data.iterrows():
        if(data.iloc[index_data,6]==teamsData.iloc[index_teams,2]):
            val1=data.iloc[index_data,9]
            val2+=val1
        elif(data.iloc[index_data,7]==teamsData.iloc[index_teams,2]):
            val1=data.iloc[index_data,10]
            val2+=val1
    
    teamsData.iloc[index_teams,1]=val2


# In[274]:


print(teamsData.sort_values(by='Teams'))


# In[276]:


sns.barplot(x='Teams',y='Goal Difference',data=teamsData)
plt.xticks(rotation=90)
plt.show()


# In[279]:


sns.scatterplot(x='NOW',y='Goal Difference',data=teamsData)
plt.xticks(rotation=90)
plt.xlabel('Number Of Wins')
plt.show()


# In[ ]:




