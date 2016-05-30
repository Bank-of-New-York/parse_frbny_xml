# Import Modules
import xml.etree.cElementTree as ET
import urllib.request as graburl
import os
import csv
import sys

# Store Filenames
xml_filename = 'tomo_on_rrp.xml'
onrrp_csv    = 'on_rrp.csv'

# Range of dates in DDMMYYYY format
# First date available is 3.1.2016
startdate = '03012016'
enddate   = '05192016'
daterange = False

# OR you can retrieve the last n_obs number of observations
n_obs = '25'
lastn = True

if daterange == True:
    url = 'https://websvcgatewayx2.frbny.org/autorates_tomo_external/services/v1_0/tomo/retrieve?f='+ startdate + '&t=' + enddate
    graburl.urlretrieve(url,xml_filename)
    
elif lastn == True:
    url = 'https://websvcgatewayx2.frbny.org/autorates_tomo_external/services/v1_0/tomo/retrieveXmlLastN?n=' + n_obs
    graburl.urlretrieve(url,xml_filename)

## Parse the XML
tree = ET.parse(xml_filename)
root = tree.getroot()

# Namespace
ns2 = 'http://www.newyorkfed.org/xml/schemas/repoCrossSection'

data = root.findall(".//*{" + ns2 + "}Group[@operationType='RRP']")

dates       = []
mat_dates   = []
acc_cp      = []
part_cp     = []
op_term     = []
op_biz_term = []
method      = []
val_acc     = []
val_sub     = []

for element in data:
    dates.append(element.attrib['dealDate'])
    mat_dates.append(element.attrib['maturityDate'])
    acc_cp.append(element.attrib['acceptedCounterparties'])
    part_cp.append(element.attrib['participatingCounterparties'])
    op_term.append(element.attrib['operationTerm'])
    op_biz_term.append(element.attrib['operationBusinessTerm'])
    method.append(element.attrib['auctionMethod'])

    data2 = element.findall("{"+ns2+"}Section[@repoMeasurementType='TPA']/{"+ns2+"}totalPropositionsAccepted")
    for element2 in data2:
        val_acc.append(element2.attrib['value'])

    data3 = element.findall("{"+ns2+"}Section[@repoMeasurementType='TPS']/{"+ns2+"}totalPropositionsSubmitted")
    for element3 in data3:
        val_sub.append(element3.attrib['value'])

forexport = [dates,
             mat_dates,
             acc_cp,
             part_cp,
             op_term,
             op_biz_term,
             method,
             val_acc,
             val_sub]

# Use zip to reshape the data for exporting to csv
forexport = list(zip(forexport[0],forexport[1],forexport[2],forexport[3],forexport[4],forexport[5],forexport[6],forexport[7],forexport[8]))

# Write to .csv file
with open(onrrp_csv, 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile)
    varnames = ['Date',
                'Maturity_Date',
                'Number_cp_accepted',
                'Number_cp_participated',
                'Term_of_operation',
                'Business_term',
                'Method',
                'Value_accepted',
                'Value_submitted']
    writer.writerow(varnames)
    writer.writerows(forexport)


