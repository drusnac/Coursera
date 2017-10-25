Jupyter Notebook Logout Control PanelAssignment 4 Last Checkpoint: a minute ago (autosaved) 
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
You are currently looking at version 1.1 of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the Jupyter Notebook FAQ course resource.
In [2]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
Assignment 4 - Hypothesis Testing
This assignment requires more individual learning than previous assignments - you are encouraged to check out the pandas documentation to find functions or methods you might not have used yet, or ask questions on Stack Overflow and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
Definitions:
A quarter is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
A recession is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
A recession bottom is the quarter within a recession which had the lowest GDP.
A university town is a city which has a high percentage of university students compared to the total population of the city.
Hypothesis: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (price_ratio=quarter_before_recession/recession_bottom)
The following data files are available for this assignment:
From the Zillow research data site there is housing data for the United States. In particular the datafile for all homes at a city level, City_Zhvi_AllHomes.csv, has median home sale prices at a fine grained level.
From the Wikipedia page on college towns is a list of university towns in the United States which has been copy and pasted into the file university_towns.txt.
From Bureau of Economic Analysis, US Department of Commerce, the GDP over time of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file gdplev.xls. For this assignment, only look at GDP data from the first quarter of 2000 onward.
Each function in this assignment below is worth 10%, with the exception of run_ttest(), which is worth 50%.
#City_Zhvi_AllHomes.csv
#AllHomes = pd.read_excel('Energy Indicators.xls', #sheetname='Energy',skiprows=17,skipfooter=38) AllHomes = pd.read_csv('City_Zhvi_AllHomes.csv', index_col=0, skiprows=1)
In [3]:

#
# Use this dictionary to map state names to two letter acronyms
AllHomes = pd.read_csv('City_Zhvi_AllHomes.csv', index_col=0, skiprows=0)
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
#AllHomes.head()
​
#data = pd.read_csv('university_towns.txt', sep=" ", header=None)
#data = pd.read_csv('university_towns.txt')
​
​
#GDP Levels
GDPlevels = pd.read_excel('gdplev.xls',sheetname='Sheet1', skiprows=219)
GDPlevels = GDPlevels[['1999q4', 9926.1]]
#GDPlevels.drop(GDPlevels.columns[[0, 1, 2,3,5,7]], axis=1,inplace=True)
GDPlevels.columns = ['Quarter','GDP']
​
​
​
#data
pd.set_option('display.max_rows', None)  
​
#GDPlevels
​
In [4]:

def get_list_of_university_towns():
    data = pd.read_fwf('university_towns.txt', header=None)
    newData = data
    newData.columns = ['Raw']
    #newData['State'] = ''
    #newData['RegionName'] = ''
    newData['State'] = newData[newData['Raw'].str.contains("edit")]
    StateIds = newData['State'].str.replace('\[edit\]', '')
    newData['State'] = StateIds
    newData.fillna(method='ffill',inplace=True)
    RegionIDs = newData['Raw'].str.split('\s\(') # split the index by '('
    newData['RegionName'] = RegionIDs.str[0]
    
    #print(newData[newData['RegionName'].str.contains("edit")])
    newData = (newData[~newData['RegionName'].str.contains("edit")])
    newData = newData.drop('Raw', 1)
​
    #newData.drop(newData[newData['RegionName'].str.contains("edit")], axis=1,inplace=True)
    
    #newData['Raw'].str.replace('Alabama','TEST')
    #newData = newData.replace({'edit': 'DDDD'})
    #StateIds = newData['State'].str.split('\s\[') # split the index by '('
​
    #newData['data'] = np.where(df.Col2 == 'specific value', df.Col1, df.Col2)
    #print(newData[newData['Raw'].str.contains("edit")])
    
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:
​
    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    return newData
    #return RegionIDs
#get_list_of_university_towns()
In [5]:

#
def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    GDPAmount = GDPlevels['GDP']
    for i in range(2,len(GDPAmount)):
        m2GDP = GDPlevels.get_value(i-2,'GDP')
        m1GDP = GDPlevels.get_value(i-1,'GDP')
        m0GDP = GDPlevels.get_value(i-0,'GDP')
        if m0GDP < m1GDP and  m1GDP < m2GDP:
            recessionStart = GDPlevels.get_value(i-2,'Quarter')
            break;
    return recessionStart
#get_recession_start()
In [6]:

#
def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    recessionStart = get_recession_start()
    GDPAmount = GDPlevels['GDP']
    for i in range(0,len(GDPAmount)-2):
        #m2GDP = GDPlevels.get_value(i-2,'GDP in 2009 dollars')
        #m1GDP = GDPlevels.get_value(i-1,'GDP in 2009 dollars')
        m0GDP = GDPlevels.get_value(i-0,'GDP')
        p1GDP = GDPlevels.get_value(i+1,'GDP')
        p2GDP = GDPlevels.get_value(i+2,'GDP')
        quarterValue = GDPlevels.get_value(i,'Quarter')
        #print(m0GDP)
        if p1GDP > m0GDP and p2GDP > p1GDP and quarterValue > recessionStart:
            #print("Found Recession End")
            recessionEnd = GDPlevels.get_value(i+2,'Quarter')
            break;
   
    return recessionEnd
       
    #return "ANSWER"
#get_recession_end()
In [7]:

#
def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    recessionStart = get_recession_start()
    recessionEnd = get_recession_end()
    GDPAmount = GDPlevels['GDP']
    lowest = GDPAmount.max()
    for i in range(0,len(GDPAmount)-2):
        currentGDP = GDPlevels.get_value(i,'GDP')
        currentQuarter = GDPlevels.get_value(i,'Quarter')
        if currentGDP < lowest and currentQuarter > recessionStart and currentQuarter < recessionEnd:
            lowest = currentGDP
            lowestQuarter = currentQuarter
            #print(lowest)
            #break;    
    return lowestQuarter
#get_recession_bottom()
In [8]:

#
def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    AllHomesLocal = pd.read_csv('City_Zhvi_AllHomes.csv', index_col=0, skiprows=0)
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    AllHomesLocal.replace({'State': states}, inplace=True)
    #columnsToRemove = AllHomes.columns
    #GDPlevels.drop(GDPlevels.columns[[0, 1, 2,3,5,7]], axis=1,inplace=True)
    #AllHomesLocal = AllHomesLocal[['RegionName', 'State','Metro','CountyName','SizeRank']]
    AllHomesRegions = AllHomesLocal[['State', 'RegionName']]
    #housingDates = AllHomesLocal[['2000-01':'2016-08']]
    housingDates = AllHomesLocal.loc[:, '2000-01':'2016-08']
    housingDates.columns = pd.to_datetime(housingDates.columns)
    housingDates = housingDates.resample('Q',axis=1).mean()
    housingDates = housingDates.rename(columns=lambda x: str(x.to_period('Q')).lower())
    
    mergedDf = pd.merge(AllHomesRegions, housingDates, how='outer', left_index=True, right_index=True)
    #mergedDf.index()
    mergedDf.set_index(['State', 'RegionName'],inplace=True)
    
    #return housingDates.shape
    return  mergedDf
#convert_housing_data_to_quarters()
#AllHomes.size()
In [12]:

def run_ttest():
    from scipy import stats
    #stats.ttest_ind?
    '''First create new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. 
    
    Then runs a ttest comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). 
    
    The variable p should be equal to the exact p value returned from scipy.stats.ttest_ind(). 
    
    The value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    housingCopy = convert_housing_data_to_quarters()
    housingGrowth = housingCopy.loc[:, get_recession_start():get_recession_bottom()]
    housingGrowth['priceChange'] = housingGrowth['2009q1'] - housingGrowth['2008q3']
    #housingGrowth = housingGrowth.sort(priceChange.index, ascending=0)
    housingGrowth.sort_index(axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last')
    uniTowns = get_list_of_university_towns()
    uniTowns['uniTown'] = int(1)
    uniTowns.set_index(['State', 'RegionName'],inplace=True)
    #left_on='lkey', right_on='rkey'
    
    df = pd.merge(housingGrowth, uniTowns, how='outer', left_index=True, right_index=True)
    df['uniTown'] = df['uniTown'].fillna(value=0)
    def set_price_ratio(row):
        return (row['2008q3'] - row['2009q2'])/row['2008q3']
    
    df['PriceRatio'] = df.apply(set_price_ratio,axis=1)
    
    
    collegeTownDecline = df[df['uniTown'] == 1].dropna()
    noncollegeTownDecline = df[df['uniTown'] != 1].dropna()
    
​
    results = stats.ttest_ind(collegeTownDecline['PriceRatio'], noncollegeTownDecline['PriceRatio'])
    statistic = results[0]
    pvalue = results[1]
    if pvalue < 0.01:
        different=True
    else:
        different=False
        
    if collegeTownDecline['PriceRatio'].mean() <  noncollegeTownDecline['PriceRatio'].mean():
        better = 'university town'
    else:
        better = "non-university town"
    
    
    finalResults = (different, pvalue, better )
    return finalResults
    return df.head()
run_ttest()
Out[12]:
(True, 0.0089755875407126953, 'university town')
In [ ]:

​
In [ ]:

​
