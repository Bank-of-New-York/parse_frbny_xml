# Import Modules
import xml.etree.cElementTree as ET
import urllib.request as graburl
import os
import csv
import sys

# Store Filenames
rates_xml = 'obfr_rates.xml'
vol_xml   = 'obfr_volume.xml'
obfr_csv  = 'obfr.csv'

# Range of dates in DDMMYYYY format
# First date available is 3.1.2016
startdate = '03012016'
enddate   = '05192016'
daterange = False

# OR you can retrieve the last n_obs number of observations
n_obs = '25'
lastn = True

if daterange == True:
    # Source for Rates
    url_rates = 'https://websvcgatewayx2.frbny.org/autorates_obfr_external/services/v1_0/obfr/xml/retrieve?typ=RATE&f=' + startdate + '&t=' + enddate
    graburl.urlretrieve(url_rates,rates_xml)

    # Source for Volume
    url_vol = 'https://websvcgatewayx2.frbny.org/autorates_obfr_external/services/v1_0/obfr/xml/retrieve?typ=VOLUME&f=' + startdate + '&t=' + enddate
    graburl.urlretrieve(url_vol,vol_xml)
    
elif lastn == True:
    # Source for Rates
    url_rates = 'https://websvcgatewayx2.frbny.org/autorates_obfr_external/services/v1_0/obfr/xml/retrieveLastN?n=' + n_obs + '&typ=RATE'
    graburl.urlretrieve(url_rates,rates_xml)
    # Source for Volume
    url_vol = 'https://websvcgatewayx2.frbny.org/autorates_obfr_external/services/v1_0/obfr/xml/retrieveLastN?n=' + n_obs + '&typ=VOLUME'
    graburl.urlretrieve(url_vol,vol_xml)    

## RATES
# Parse the XML
tree = ET.parse(rates_xml)
root = tree.getroot()

# List to loop over percentiles
ratelist = ['1%','25%','50%','75%','99%']
# Counter for loop
iter = 1

for rate in ratelist:
    print(rate)
    data = root.findall(".//*[@FUNDRATE_OBS_POINT=\'"+rate+"\']/Obs")

    dates = []
    rates = []

    for element in data:
        dates.append(element.attrib['TIME_PERIOD'])
        rates.append(element.attrib['OBS_VALUE'])

    if iter == 1:
        forexport = [dates,rates]

    # sanity check to make sure the dates match
    elif forexport[0] == dates:
        forexport.append(rates)

    else:
        print("Oops! The dates don't match up.")
        sys.exit("Oops! The dates don't match up.")

    iter = iter + 1

## VOLUME
# Parse the XML
tree = ET.parse(vol_xml)
root = tree.getroot()

data_vol = root.findall(".//Series[@FUNDRATE_SUPPLEMENTAL='VOLUME']/Obs")

print("Volume")

dates = []
vol   = []

for element in data_vol:
    dates.append(element.attrib['TIME_PERIOD'])
    vol.append(element.attrib['OBS_VALUE'])

# sanity check to make sure the dates match
if forexport[0] == dates:
    forexport.append(vol)

else:
    print("Oops! The dates don't match up.")
    sys.exit("Oops! The dates don't match up.")

# Use zip to reshape the data for exporting to csv
forexport = list(zip(forexport[0],forexport[1],forexport[2],forexport[3],forexport[4],forexport[5],forexport[6]))

# Write to .csv file
with open(obfr_csv, 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile)
    varnames = ['Date','1%','25%','Median','75%','99%','Volume']
    writer.writerow(varnames)
    writer.writerows(forexport)


