import sqlite3
import time
import zlib
import string
from collections import OrderedDict
from operator import itemgetter, attrgetter

conn = sqlite3.connect('terror_content.sqlite')
cur = conn.cursor()

cur.execute('SELECT id, countryID, countryText FROM Terrorism2')
subjects = dict()
countriesDict = {}
for record in cur :
    currentCountryID = record[1]
    currentCountryName = record[2]
    if currentCountryID in countriesDict:
        terrorCount = countriesDict[currentCountryID]
        countriesDict[currentCountryID] = terrorCount+1
    else:
        countriesDict[currentCountryID] = 1


#Binning of Countries
totalCountries = len(countriesDict)
print("Total Countries: " + str(totalCountries))
print(countriesDict)
sortedCountryDict = sorted(countriesDict.items(), key=itemgetter(1), reverse=False)
print(sortedCountryDict)
totalBins = 8
binSize = int(totalCountries/totalBins)
binDivider = []
for x in range(0,totalBins-1):
    dividerNum = binSize*(x+1)
    print(sortedCountryDict[dividerNum])
    binDivider.append(sortedCountryDict[dividerNum][1])
print(binDivider)

print(OrderedDict(sorted(countriesDict.items(), key=itemgetter(1), reverse=False)))

#for key, value in sorted(countriesDict.items(), key=itemgetter(1), True):
#    print(key, value)
#for key, value in sorted(countriesDict.iteritems(), key=lambda (k,v): (v,k)):

#for country in countriesDict:
    #print(country)
#    if country not in countryIDs:
#        #print("MISSING COUNTRY ID:")
#        print('"' + country + '": ' + '"')

#Get Max Indidents
maxIndidents = 0
for country in countriesDict:
    if countriesDict[country] > maxIndidents:
        maxIndidents = countriesDict[country]
print("Max Indicents: " + str(maxIndidents))

#Write Out Javascript file to use for html
fhand = open('main2.js','w')
fhand.write( "var map = new Datamap({scope: 'world',element: document.getElementById('container1'),projection: 'mercator',height: 800,fills: {defaultFill: '#D3D3D3',")
fhand.write( "\n")
fhand.write("L1: '#ffffcc',")
fhand.write("L2: '#ffff99',")
fhand.write("L3: '#ffff66',")
fhand.write("L4: '#ffcc00',")
fhand.write("L5: '#ff9933',")
fhand.write("L6: '#ff6600',")
fhand.write("L7: '#ff5050',")
fhand.write("L8: '#cc0000',")
fhand.write("lt50: 'rgba(0,244,244,0.9)',")
fhand.write("gt50: 'blue',")
fhand.write("highlight: 'green'")
fhand.write("},")
fhand.write( "\n\n")
fhand.write("data: {\n")

skipCountries = {"Dominica","Bahrain","Guadeloupe","Mauritius","Seychelles","Antigua and Barbuda","Martinique",
                 "Bahamas","Malta","Barbados","Grenada","New Hebrides","Bosnia-Herzegovina","St. Kitts and Nevis",
                 "Wallis and Futuna","Macau","French Polynesia","Comoros","Slovak Republic","St. Lucia","Guinea-Bissau",
                 "International","Serbia-Montenegro"}
for country in countriesDict:
    #if country not in skipCountries:
        if countriesDict[country] < binDivider[0]:
            fhand.write(country + ": {fillKey: 'L1', attacks: " + str(countriesDict[country]) + "},\n")
        if countriesDict[country] >= binDivider[0] and countriesDict[country] < binDivider[1]:
            fhand.write(country + ": {fillKey: 'L2', attacks: " + str(countriesDict[country]) + "},\n")
        if countriesDict[country] >= binDivider[1] and countriesDict[country] < binDivider[2]:
            fhand.write(country + ": {fillKey: 'L3', attacks: " + str(countriesDict[country]) + "},\n")
        if countriesDict[country] >= binDivider[2] and countriesDict[country] < binDivider[3]:
            fhand.write(country + ": {fillKey: 'L4', attacks: " + str(countriesDict[country]) + "},\n")
        if countriesDict[country] >= binDivider[3] and countriesDict[country] < binDivider[4]:
            fhand.write(country + ": {fillKey: 'L5', attacks: " + str(countriesDict[country]) + "},\n")
        if countriesDict[country] >= binDivider[4] and countriesDict[country] < binDivider[5]:
            fhand.write(country + ": {fillKey: 'L6', attacks: " + str(countriesDict[country]) + "},\n")
        if countriesDict[country] >= binDivider[5] and countriesDict[country] < binDivider[6]:
            fhand.write(country + ": {fillKey: 'L7', attacks: " + str(countriesDict[country]) + "},\n")
        if countriesDict[country] > binDivider[6]:
            fhand.write(country + ": {fillKey: 'L8', attacks: " + str(countriesDict[country]) + "},\n")
fhand.write("},\n")
fhand.write("geographyConfig: {popupTemplate: function(geo, data) {return ['<div class=\"hoverinfo\"><strong>',geo.properties.name,': ' + data.attacks,'</strong></div>'].join('');}}")
fhand.write("\n")

fhand.write( "});\n")

fhand.close()

print("Output written to main.js")
print("Open worldmap.html in a browser to see the vizualization")


