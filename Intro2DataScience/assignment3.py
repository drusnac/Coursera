
You are currently looking at version 1.5 of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the Jupyter Notebook FAQ course resource.
Assignment 3 - More Pandas
This assignment requires more individual learning then the last one did - you are encouraged to check out the pandas documentation to find functions or methods you might not have used yet, or ask questions on Stack Overflow and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

-
### Question 1 (20%)
Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
​
Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
​
`['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
​
Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
​
Rename the following list of countries (for use in later questions):
​
```"Republic of Korea": "South Korea",
"United States of America": "United States",
"United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
"China, Hong Kong Special Administrative Region": "Hong Kong"```
​
There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
​
e.g. 
​
`'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
​
`'Switzerland17'` should be `'Switzerland'`.
​
<br>
​
Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
​
Make sure to skip the header, and rename the following list of countries:
​
```"Korea, Rep.": "South Korea", 
"Iran, Islamic Rep.": "Iran",
"Hong Kong SAR, China": "Hong Kong"```
​
<br>
​
Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
​
Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
​
The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
       'Citations per document', 'H index', 'Energy Supply',
       'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
       '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
​
*This function should return a DataFrame with 20 columns and 15 entries.*
​
​
In [358]:

-
import pandas as pd
import numpy as np
import re
​
energy = pd.read_excel('Energy Indicators.xls', sheetname='Energy',skiprows=17,skipfooter=38)
energy = energy.drop('Unnamed: 0', 1)
energy = energy.drop('Unnamed: 1', 1)
energy.columns=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
energy = energy.replace('...', np.nan)
energy['Energy Supply'] = energy['Energy Supply']*1000000
#Remove Numbers from Countries
names_ids2 = energy['Country'].str.replace('[0-9]','') # split the index by '('
energy['Country'] = names_ids2
names_ids = energy['Country'].str.split('\s\(') # split the index by '('
energy['Country'] = names_ids.str[0]
#Rename Certain Countires
energy = energy.replace({"Republic of Korea": "South Korea",
    "United States of America": "United States",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "China, Hong Kong Special Administrative Region": "Hong Kong"})
energy = energy.set_index(['Country'])
​
​
#Load World Bank Data
GDP = pd.read_csv('world_bank.csv', index_col=0, skiprows=4)
GDP.index.name = 'Country'
GDP.rename(index={"Korea, Rep.": "South Korea", 
    "Iran, Islamic Rep.": "Iran",
    "Hong Kong SAR, China": "Hong Kong"},inplace=True)
​
#Load SCIMAGO data
ScimEn = pd.read_excel('scimagojr-3.xlsx',skiprows=0)
ScimEn = ScimEn.set_index(['Country'])
​
#Merge Set
merged = pd.merge(energy, GDP, how='outer', left_index=True, right_index=True)
merged2 = pd.merge(merged, ScimEn, how='outer', left_index=True, right_index=True)
#print(energy.shape)
​
​
​
def answer_one():
    merged2Ranks = merged2[(merged2['Rank'] < 16 )]
    mergedTop15 = merged2Ranks[['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
       'Citations per document', 'H index', 'Energy Supply',
       'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
       '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    
    #Type cast to int64 to match grader
    mergedTop15['Rank'] = mergedTop15['Rank'].astype(np.int64)
    mergedTop15['Documents'] = mergedTop15['Documents'].astype(np.int64)
    mergedTop15['Citable documents'] = mergedTop15['Citable documents'].astype(np.int64)
    mergedTop15['Citations'] = mergedTop15['Citations'].astype(np.int64)
    mergedTop15['Self-citations'] = mergedTop15['Self-citations'].astype(np.int64)
    mergedTop15['H index'] = mergedTop15['H index'].astype(np.int64)
    return mergedTop15
​
answer_one()
#pd.set_option('display.max_rows', None)  
#GDP
​
Out[358]:
Rank	Documents	Citable documents	Citations	Self-citations	Citations per document	H index	Energy Supply	Energy Supply per Capita	% Renewable	2006	2007	2008	2009	2010	2011	2012	2013	2014	2015
Country																				
Australia	14	8831	8725	90765	15606	10.28	107	5.386000e+09	231.0	11.810810	1.021939e+12	1.060340e+12	1.099644e+12	1.119654e+12	1.142251e+12	1.169431e+12	1.211913e+12	1.241484e+12	1.272520e+12	1.301251e+12
Brazil	15	8668	8596	60702	14396	7.00	86	1.214900e+10	59.0	69.648030	1.845080e+12	1.957118e+12	2.056809e+12	2.054215e+12	2.208872e+12	2.295245e+12	2.339209e+12	2.409740e+12	2.412231e+12	2.319423e+12
Canada	6	17899	17620	215003	40930	12.01	149	1.043100e+10	296.0	61.945430	1.564469e+12	1.596740e+12	1.612713e+12	1.565145e+12	1.613406e+12	1.664087e+12	1.693133e+12	1.730688e+12	1.773486e+12	1.792609e+12
China	1	127050	126767	597237	411683	4.70	138	1.271910e+11	93.0	19.754910	3.992331e+12	4.559041e+12	4.997775e+12	5.459247e+12	6.039659e+12	6.612490e+12	7.124978e+12	7.672448e+12	8.230121e+12	8.797999e+12
France	9	13153	12973	130632	28601	9.93	114	1.059700e+10	166.0	17.020280	2.607840e+12	2.669424e+12	2.674637e+12	2.595967e+12	2.646995e+12	2.702032e+12	2.706968e+12	2.722567e+12	2.729632e+12	2.761185e+12
Germany	7	17027	16831	140566	27426	8.26	126	1.326100e+10	165.0	17.901530	3.332891e+12	3.441561e+12	3.478809e+12	3.283340e+12	3.417298e+12	3.542371e+12	3.556724e+12	3.567317e+12	3.624386e+12	3.685556e+12
India	8	15005	14841	128763	37209	8.58	115	3.319500e+10	26.0	14.969080	1.265894e+12	1.374865e+12	1.428361e+12	1.549483e+12	1.708459e+12	1.821872e+12	1.924235e+12	2.051982e+12	2.200617e+12	2.367206e+12
Iran	13	8896	8819	57470	19125	6.46	72	9.172000e+09	119.0	5.707721	3.895523e+11	4.250646e+11	4.289909e+11	4.389208e+11	4.677902e+11	4.853309e+11	4.532569e+11	4.445926e+11	4.639027e+11	NaN
Italy	11	10964	10794	111850	26661	10.20	106	6.530000e+09	109.0	33.667230	2.202170e+12	2.234627e+12	2.211154e+12	2.089938e+12	2.125185e+12	2.137439e+12	2.077184e+12	2.040871e+12	2.033868e+12	2.049316e+12
Japan	3	30504	30287	223024	61554	7.31	134	1.898400e+10	149.0	10.232820	5.496542e+12	5.617036e+12	5.558527e+12	5.251308e+12	5.498718e+12	5.473738e+12	5.569102e+12	5.644659e+12	5.642884e+12	5.669563e+12
Russian Federation	5	18534	18301	34266	12422	1.85	57	3.070900e+10	214.0	17.288680	1.385793e+12	1.504071e+12	1.583004e+12	1.459199e+12	1.524917e+12	1.589943e+12	1.645876e+12	1.666934e+12	1.678709e+12	1.616149e+12
South Korea	10	11983	11923	114675	22595	9.57	104	1.100700e+10	221.0	2.279353	9.410199e+11	9.924316e+11	1.020510e+12	1.027730e+12	1.094499e+12	1.134796e+12	1.160809e+12	1.194429e+12	1.234340e+12	1.266580e+12
Spain	12	9428	9330	123336	23964	13.08	115	4.923000e+09	106.0	37.968590	1.414823e+12	1.468146e+12	1.484530e+12	1.431475e+12	1.431673e+12	1.417355e+12	1.380216e+12	1.357139e+12	1.375605e+12	1.419821e+12
United Kingdom	4	20944	20357	206091	37874	9.84	139	7.920000e+09	124.0	10.600470	2.419631e+12	2.482203e+12	2.470614e+12	2.367048e+12	2.403504e+12	2.450911e+12	2.479809e+12	2.533370e+12	2.605643e+12	2.666333e+12
United States	2	96661	94747	792274	265436	8.20	230	9.083800e+10	286.0	11.570980	1.479230e+13	1.505540e+13	1.501149e+13	1.459484e+13	1.496437e+13	1.520402e+13	1.554216e+13	1.577367e+13	1.615662e+13	1.654857e+13
Question 2 (6.6%)
The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
This function should return a single number.
In [161]:

%%HTML
<svg width="800" height="300">
  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />
  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />
  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />
  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>
  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>
</svg>
Everything but this!
In [359]:

def answer_two():
    
    mergedOuter = pd.merge(pd.merge(energy, GDP, how='outer', left_index=True, right_index=True), ScimEn, how='outer', left_index=True, right_index=True)
    mergedInner = pd.merge(pd.merge(energy, GDP, left_index=True, right_index=True), ScimEn, left_index=True, right_index=True)

    return len(mergedOuter) - len(mergedInner)
answer_two()
def answer_two():
    
    mergedOuter = pd.merge(pd.merge(energy, GDP, how='outer', left_index=True, right_index=True), ScimEn, how='outer', left_index=True, right_index=True)
    mergedInner = pd.merge(pd.merge(energy, GDP, left_index=True, right_index=True), ScimEn, left_index=True, right_index=True)
​
    return len(mergedOuter) - len(mergedInner)
answer_two()
Out[359]:
156

<br>
​
## Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

### Question 3 (6.6%)
What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
​
*This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*
In [369]:

def answer_three():
    Top15 = answer_one()
    columns = ['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015',]
    avg = Top15.groupby(level=0)[columns].agg({'avgGDP': np.average, 'sum': np.sum})
    Top15['sum'] = Top15[columns].sum(axis=1)
    Top15['avg'] = Top15[columns].mean(axis=1)
    results = Top15.sort(['avg'], ascending=0)
    avgGDP = results['avg']
    return avgGDP
answer_three()
Out[369]:
Country
United States         1.536434e+13
China                 6.348609e+12
Japan                 5.542208e+12
Germany               3.493025e+12
France                2.681725e+12
United Kingdom        2.487907e+12
Brazil                2.189794e+12
Italy                 2.120175e+12
India                 1.769297e+12
Canada                1.660647e+12
Russian Federation    1.565459e+12
Spain                 1.418078e+12
Australia             1.164043e+12
South Korea           1.106715e+12
Iran                  4.441558e+11
Name: avg, dtype: float64
Question 4 (6.6%)
By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
This function should return a single number.
In [197]:

def answer_four():
    Top15 = answer_one()
    columns = ['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015',]
    #avg = Top15.groupby(level=0)[columns].agg({'avgGDP': np.average, 'sum': np.sum})
    Top15['sum'] = Top15[columns].sum(axis=1)
    Top15['avg'] = Top15['sum']/10
    
    sortedavg = Top15.sort(['avg'], ascending=0, na_position='last')
    
    
    sixthLargest = sortedavg.iloc[5]
    sixthLargest['2006'] - sixthLargest['2015']
​
    return sixthLargest['2015'] - sixthLargest['2006']
    #return sortedavg
answer_four()
Out[197]:
246702696075.3999
Question 5 (6.6%)
What is the mean Energy Supply per Capita?
This function should return a single number.
In [201]:

#
def answer_five():
    Top15 = answer_one()
    #Top15 = Top15.fillna(0)
    return Top15['Energy Supply per Capita'].mean()
    #return  Top15['Energy Supply per Capita']
answer_five()
Out[201]:
150.30769230769232
Question 6 (6.6%)
What country has the maximum % Renewable and what is the percentage?
This function should return a tuple with the name of the country and the percentage.
In [7]:

def answer_six():
    Top15 = answer_one()
    sortedRN = Top15.sort(['% Renewable'], ascending=0, na_position='last')
    #sortedRN['% Renewable']
    #sortedRN.name
    #return sortedRN['% Renewable'][0]
    results = (sortedRN.index[0],sortedRN['% Renewable'][0])
    return results
answer_six()
Out[7]:
('Brazil', 69.648030000000006)
Question 7 (6.6%)
Create a new column that is the ratio of Self-Citations to Total Citations. What is the maximum value for this new column, and what country has the highest ratio?
This function should return a tuple with the name of the country and the ratio.
In [8]:

def answer_seven():
    Top15 = answer_one()
    Top15['Citation Ratio'] = Top15['Self-citations'] / Top15['Citations']
    sortedRN = Top15.sort(['Citation Ratio'], ascending=0, na_position='last')
    results = (sortedRN.index[0],sortedRN['Citation Ratio'][0])
​
    return results
answer_seven()
Out[8]:
('China', 0.68931261793894216)
Question 8 (6.6%)
Create a column that estimates the population using Energy Supply and Energy Supply per capita. What is the third most populous country according to this estimate?
This function should return a single string value.
In [183]:

    Top15['PopEstimate'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']

def answer_eight():
    Top15 = answer_one()
    Top15['PopEstimate'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    sortedRN = Top15.sort(['PopEstimate'], ascending=0, na_position='last')
​
    #results = (sortedRN.index[0],sortedRN['PopEstimate'][0])
    results = sortedRN.index[2]
​
    return results
answer_eight()
Out[183]:
'Brazil'

### Question 9 (6.6%)
Create a column that estimates the number of citable documents per person. 
What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
​
*This function should return a single number.*
​
*(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*
In [160]:

#
def answer_nine():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents']/Top15['PopEst']
    #DataFrame.corr(method='pearson', min_periods=1)[source]
    #Top15.fillna(0)
    #Top15['Citable docs per Capita'].corr(Top15['Energy Supply per Capita'])
    #Top15['corr']
    #return Top15
    return Top15['Citable docs per Capita'].corr(Top15['Energy Supply per Capita'])
    #return Top15
answer_nine()
Out[160]:
0.86428997688544074
In [17]:

    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']

def plot9():
    import matplotlib as plt
    %matplotlib inline
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])
#plot9()    
In [ ]:

#plot9() # Be sure to comment out plot9() before submitting the assignment!

### Question 10 (6.6%)
Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
​
*This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*
In [267]:

#
def answer_ten():
    Top15 = answer_one()
    medianValue = Top15['% Renewable'].median()
    Top15['HighRenew'] = 0
    
    Top15.loc[Top15['% Renewable'] > medianValue, 'HighRenew'] = 1
    #df.loc[df['x'] > 2, 'y'] = -1
    #Top15['HighRenew'].apply(lambda x: 'true' if x <= 2.5 else 'false')
    Top15['HighRenew'] = Top15['% Renewable'].apply(lambda x: 1 if x >= medianValue else 0)
​
    #if Top15['% Renewable'] > medianValue:
    #    Top15['HighRenew'] = 1
    #else:
    #    Top15['HighRenew'] = 0
    
    HighRenew = Top15.sort(['HighRenew'], ascending=1, na_position='last')
    return HighRenew['HighRenew']
    #return Top15
answer_ten()
Out[267]:
Country
Australia             0
India                 0
Iran                  0
Japan                 0
South Korea           0
United Kingdom        0
United States         0
Brazil                1
Canada                1
China                 1
France                1
Germany               1
Italy                 1
Russian Federation    1
Spain                 1
Name: HighRenew, dtype: int64

### Question 11 (6.6%)
Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
​
```python
ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
```
​
*This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*
In [386]:

    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']    

ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
def answer_eleven():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']    
    continentDf = pd.DataFrame(columns = ['size', 'sum', 'mean', 'std'])
    for continent, countries in Top15.groupby(ContinentDict):
        continentDf.loc[continent] = [len(countries), countries['PopEst'].sum(),countries['PopEst'].mean(),countries['PopEst'].std()]
    return continentDf
answer_eleven()
Out[386]:
size	sum	mean	std
Asia	5.0	2.898666e+09	5.797333e+08	6.790979e+08
Australia	1.0	2.331602e+07	2.331602e+07	NaN
Europe	6.0	4.579297e+08	7.632161e+07	3.464767e+07
North America	2.0	3.528552e+08	1.764276e+08	1.996696e+08
South America	1.0	2.059153e+08	2.059153e+08	NaN

### Question 12 (6.6%)
Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
​
*This function should return a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*
In [416]:

def answer_twelve():
    Top15 = answer_one()
    Top15 = Top15.reset_index()
    Top15['Continent'] = '0'
    def f(row):
        #return "c{}n{}".format(row["condition"], row["no"])
        return ContinentDict[row['Country']]
        #return "c{}n{}".format(row["condition"], row["no"])
​
    Top15["Continent"] = Top15.apply(f, axis=1)   
    Top15['Bins'] = pd.cut(Top15['% Renewable'], 5)
    return Top15.groupby(['Continent','Bins']).size()
answer_twelve()
Out[416]:
Continent      Bins            
Asia           (2.212, 15.753]     4
               (15.753, 29.227]    1
Australia      (2.212, 15.753]     1
Europe         (2.212, 15.753]     1
               (15.753, 29.227]    3
               (29.227, 42.701]    2
North America  (2.212, 15.753]     1
               (56.174, 69.648]    1
South America  (56.174, 69.648]    1
dtype: int64
Question 13 (6.6%)
Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
e.g. 317615384.61538464 -> 317,615,384.61538464
This function should return a Series PopEst whose index is the country name and whose values are the population estimate string.
In [443]:

def answer_thirteen():
    Top15 = answer_one()
    Top15['PopEstimate'] = (Top15['Energy Supply']/Top15['Energy Supply per Capita'])
    Top15['PopEstimate'] = Top15['PopEstimate'].astype(np.float64)
    #Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']    
​
​
    #Top15['PopEst'] = Top15['PopEstimate'].map('{:,.2f}'.format)
    #Top15['PopEst'] = Top15['PopEst'].astype(np.int64)
    #return Top15['PopEst']
    #return Top15['PopEstimate'].map('{:,.2f}'.format)
    return Top15['PopEstimate'].map('{0:,}'.format)
​
answer_thirteen()
Out[443]:
Country
Australia              23,316,017.316017315
Brazil                 205,915,254.23728815
Canada                  35,239,864.86486486
China                 1,367,645,161.2903225
France                  63,837,349.39759036
Germany                 80,369,696.96969697
India                 1,276,730,769.2307692
Iran                    77,075,630.25210084
Italy                  59,908,256.880733944
Japan                  127,409,395.97315437
Russian Federation            143,500,000.0
South Korea            49,805,429.864253394
Spain                    46,443,396.2264151
United Kingdom         63,870,967.741935484
United States          317,615,384.61538464
Name: PopEstimate, dtype: object
Optional
Use the built in function plot_optional() to see an example visualization.
In [425]:

def plot_optional():
    import matplotlib as plt
    %matplotlib inline
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);
​
    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')
​
    print("This is an example of a visualization that can be created to help understand the data. \
This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' \
2014 GDP, and the color corresponds to the continent.")
#plot_optional()
In [ ]:

#plot_optional() # Be sure to comment out plot_optional() before submitting the assignment!
