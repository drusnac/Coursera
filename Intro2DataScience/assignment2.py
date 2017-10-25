Jupyter Notebook Logout Control PanelAssignment 2 Last Checkpoint: Last Thursday at 10:04 PM (autosaved) 
Python 3 
File
Edit
View
Insert
Cell
Kernel
Widgets
Help
CellToolbarSubmit Assignment
You are currently looking at version 1.2 of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the Jupyter Notebook FAQ course resource.
Assignment 2 - Pandas Introduction
All questions are weighted the same in this assignment.
Part 1
The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on All Time Olympic Games Medals, and does some basic data cleaning.
The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.
In [7]:

import pandas as pd
​
df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)
​
for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)
​
names_ids = df.index.str.split('\s\(') # split the index by '('
​
df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)
​
df = df.drop('Totals')
#Question 1
#df = df.sort('Gold', ascending=0)
topGold = df.iloc[0]
topGold.name
#ascending=[1, 0]
#Question 2
summerGold = df['Gold']
winterGold = df['Gold.1']
goldDelta = summerGold-winterGold
#goldDelta[0])
#largestGoldDelta = goldDelta.iloc[0]
#goldDelta
#largestGoldDelta
#winterGold.head()
​
​
df.head()
Out[7]:
# Summer	Gold	Silver	Bronze	Total	# Winter	Gold.1	Silver.1	Bronze.1	Total.1	# Games	Gold.2	Silver.2	Bronze.2	Combined total	ID
Afghanistan	13	0	0	2	2	0	0	0	0	0	13	0	0	2	2	AFG
Algeria	12	5	2	8	15	3	0	0	0	0	15	5	2	8	15	ALG
Argentina	23	18	24	28	70	18	0	0	0	0	41	18	24	28	70	ARG
Armenia	5	1	2	9	12	6	0	0	0	0	11	1	2	9	12	ARM
Australasia	2	3	4	5	12	0	0	0	0	0	2	3	4	5	12	ANZ
Question 0 (Example)
What is the first country in df?
This function should return a Series.
In [ ]:

# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
​
def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[0]
​
# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
answer_zero() 
Question 1
Which country has won the most gold medals in summer games?
This function should return a single string value.
In [128]:

def answer_one():
    dfsorted = df.sort('Gold', ascending=0)
    return dfsorted.iloc[0].name
Question 2
Which country had the biggest difference between their summer and winter gold medal counts?
This function should return a single string value.
In [129]:

def answer_two():
    summerGold = df['Gold']
    winterGold = df['Gold.1']
    df['goldDelta'] = summerGold-winterGold
    dfgold = df.sort('goldDelta', ascending=0)
    dfgold.iloc[0].name
    return dfgold.iloc[0].name
Question 3
Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count?
Summer Gold−Winter GoldTotal Gold
Summer Gold−Winter GoldTotal Gold
Only include countries that have won at least 1 gold in both summer and winter.
This function should return a single string value.
In [130]:

def answer_three():
    atLeast1Gold = df[(df['Gold.1'] > 0) & (df['Gold'] > 0)]
    summerGold = atLeast1Gold['Gold']
    winterGold = atLeast1Gold['Gold.1']
    df['goldDeltaRelative'] = (summerGold-winterGold)/(summerGold+winterGold)
    dfgoldrel = df.sort('goldDeltaRelative', ascending=0)
    dfgoldrel.iloc[0].name
    return dfgoldrel.iloc[0].name
Question 4
Write a function that creates a Series called "Points" which is a weighted value where each gold medal (Gold.2) counts for 3 points, silver medals (Silver.2) for 2 points, and bronze medals (Bronze.2) for 1 point. The function should return only the column (a Series object) which you created.
This function should return a Series named Points of length 146
In [8]:

def answer_four():
    Points = df['Gold.2']*3 + df['Silver.2']*2 + df['Bronze.2']*1
    #print(Points)
    return Points
df.head()
answer_four()
Out[8]:
Afghanistan                            2
Algeria                               27
Argentina                            130
Armenia                               16
Australasia                           22
Australia                            923
Austria                              569
Azerbaijan                            43
Bahamas                               24
Bahrain                                1
Barbados                               1
Belarus                              154
Belgium                              276
Bermuda                                1
Bohemia                                5
Botswana                               2
Brazil                               184
British West Indies                    2
Bulgaria                             411
Burundi                                3
Cameroon                              12
Canada                               846
Chile                                 24
China                               1120
Colombia                              29
Costa Rica                             7
Ivory Coast                            2
Croatia                               67
Cuba                                 420
Cyprus                                 2
                                    ... 
Spain                                268
Sri Lanka                              4
Sudan                                  2
Suriname                               4
Sweden                              1217
Switzerland                          630
Syria                                  6
Chinese Taipei                        32
Tajikistan                             4
Tanzania                               4
Thailand                              44
Togo                                   1
Tonga                                  2
Trinidad and Tobago                   27
Tunisia                               19
Turkey                               191
Uganda                                14
Ukraine                              220
United Arab Emirates                   3
United States                       5684
Uruguay                               16
Uzbekistan                            38
Venezuela                             18
Vietnam                                4
Virgin Islands                         2
Yugoslavia                           171
Independent Olympic Participants       4
Zambia                                 3
Zimbabwe                              18
Mixed team                            38
dtype: int64
Part 2
For the next set of questions, we will be using census data from the United States Census Bureau. Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. See this document for a description of the variable names.
The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.
Question 5
Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
This function should return a single string value.
In [38]:

def answer_five():
    census_df = pd.read_csv('census.csv')
    census_df.head()
    states = census_df[census_df['SUMLEV'] == 40]
    states['top3Pop'] = 0
    newStates = states.set_index(['STNAME'])
    counties = census_df[census_df['SUMLEV'] == 50]
    maxCounties = 0
    maxState = ''
    for state in states['STNAME']:
        countyCount = counties[(counties['STNAME'] == state)]
        countyCount = countyCount.sort('CENSUS2010POP', ascending=0)
        topCountySum = sum(countyCount['CENSUS2010POP'].iloc[0:3])
   
        newStates.loc[state,'top3Pop'] = topCountySum
    
   
        if len(countyCount) > maxCounties:
            maxState = state
            maxCounties = len(countyCount)
    topStates = newStates.sort('top3Pop', ascending=0)
    print(topStates.index[0:3])
    totalStatePop = []
    for statePop in topStates.index[0:3]:
        totalStatePop.append(statePop)
    print(statePop)
    print(type(totalStatePop))
    print("Max Counties: " + maxState)
    #topStates.head()
    return maxState
In [41]:

def answer_five():
    census_df = pd.read_csv('census.csv')
    states = census_df[census_df['SUMLEV'] == 40]
    states['top3Pop'] = 0
    newStates = states.set_index(['STNAME'])
    counties = census_df[census_df['SUMLEV'] == 50]
    maxCounties = 0
    maxState = ''
    for state in states['STNAME']:
        countyCount = counties[(counties['STNAME'] == state)]
        countyCount = countyCount.sort('CENSUS2010POP', ascending=0)
        topCountySum = sum(countyCount['CENSUS2010POP'].iloc[0:3])
        newStates.loc[state,'top3Pop'] = topCountySum
​
        if len(countyCount) > maxCounties:
            maxState = state
            maxCounties = len(countyCount)
    topStates = newStates.sort('top3Pop', ascending=0)
    print(topStates.index[0:3])
    totalStatePop = []
    for statePop in topStates.index[0:3]:
        totalStatePop.append(statePop)
    #print(type(totalStatePop))
    #print("Max Counties: " + maxState)
    print(maxState)
    return maxState
Question 6
Only looking at the three most populous counties for each state, what are the three most populous states (in order of highest population to lowest population)? Use CENSUS2010POP.
This function should return a list of string values.
In [ ]:

def answer_six():
    census_df = pd.read_csv('census.csv')
    states = census_df[census_df['SUMLEV'] == 40]
    states['top3Pop'] = 0
    newStates = states.set_index(['STNAME'])
    counties = census_df[census_df['SUMLEV'] == 50]
    maxCounties = 0
    maxState = ''
    for state in states['STNAME']:
        countyCount = counties[(counties['STNAME'] == state)]
        countyCount = countyCount.sort('CENSUS2010POP', ascending=0)
        topCountySum = sum(countyCount['CENSUS2010POP'].iloc[0:3])
        newStates.loc[state,'top3Pop'] = topCountySum
​
        if len(countyCount) > maxCounties:
            maxState = state
            maxCounties = len(countyCount)
    topStates = newStates.sort('top3Pop', ascending=0)
    print(topStates.index[0:3])
    totalStatePop = []
    for statePop in topStates.index[0:3]:
        totalStatePop.append(statePop)
    #print(type(totalStatePop))
    #print("Max Counties: " + maxState)
    print(maxState)
    return totalStatePop    
Question 7
Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.
This function should return a single string value.
In [119]:

import pandas as pd
census_df = pd.read_csv('census.csv')
​
def answer_seven():
    counties = census_df[census_df['SUMLEV'] == 50]
    counties['maxDiff'] = counties[['POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012','POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']].max(axis=1)
    counties['minDiff'] = counties[['POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012','POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']].min(axis=1)
    counties['popDiff'] = counties['maxDiff'] - counties['minDiff']
    counties = counties.sort('popDiff', ascending=0)
    return counties.iloc[0].CTYNAME
​
Harris County
Question 8
In this datafile, the United States is broken up into four regions using the "REGION" column.
Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).
In [117]:

import pandas as pd
census_df = pd.read_csv('census.csv')
​
def answer_eight():
    testQuery = census_df[(census_df['CTYNAME'].str.startswith("Washington"))]
    query = census_df[(census_df['REGION'] <= 2) & 
                      (census_df['POPESTIMATE2015'] > census_df['POPESTIMATE2014']) 
                      & (census_df['CTYNAME'].str.startswith("Washington")) == True]
    queryNew = query[['STNAME','CTYNAME']]
    return queryNew
​
​
Out[117]:
STNAME	CTYNAME
896	Iowa	Washington County
1419	Minnesota	Washington County
2345	Pennsylvania	Washington County
2355	Rhode Island	Washington County
3163	Wisconsin	Washington County
In [ ]:

​
