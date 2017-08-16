"""
Python code to upload data to Azure Search for the Custom Search example.

This script will upload all of the session information where
each individual sesssion equates to a document in an index
in an Azure Search service.

Go to http://portal.azure.com and sign up for a search service.
Get the service name and service key and plug it in below.
This is NOT production level code. Please do not use it as such.
You might have to pip install the imported modules here.

Run this script in the 'code' directory:
    python azsearch_mgmt.py

See Azure Search REST API docs for more info:
    https://docs.microsoft.com/en-us/rest/api/searchservice/index

"""

import requests
import json
import csv
import datetime
import pytz
import calendar
import os
import pyexcel as pe

# This is the service you've already created in Azure Portal
serviceName = 'your_azure_search_service_name'

# Index to be created
indexName = 'name_of_index_to_create'

# Set your service API key, either via an environment variable or enter it below
#apiKey = os.getenv('SEARCH_KEY_DEV', '')
apiKey = 'your_azure_search_service_api_key'
apiVersion = '2016-09-01'

# Input parsed content Excel file, e.g., output of step #1 in
# https://github.com/CatalystCode/CustomSearch/tree/master/JupyterNotebooks/1-content_extraction.ipynb
inputfile = os.path.join(os.getcwd(), '../sample/parsed_content.xlsx')

# Define fields mapping from Excel file column names to search index field names (except Index)
# Change this mapping to match your content fields and rename output fields as desired
# Search field names should match their definition in getIndexDefinition()
fields_map = [ ('File'            , 'File'),
               ('ChapterTitle'    , 'ChapterTitle'),
               ('SectionTitle'    , 'SectionTitle'),
               ('SubsectionTitle' , 'SubsectionTitle'),
               ('SubsectionText'  , 'SubsectionText'),
               ('Keywords'        , 'Keywords') ]

# Fields: Index	File	ChapterTitle	SectionTitle	SubsectionTitle		SubsectionText	Keywords
def getIndexDefinition():
    return {
        "name": indexName,  
        "fields": [
        {"name": "Index", "type": "Edm.String", "key": True, "retrievable": True, "searchable": False, "filterable": False, "sortable": True, "facetable": False},

        {"name": "File", "type": "Edm.String", "retrievable": True, "searchable": False, "filterable": True, "sortable": True, "facetable": False},

        {"name": "ChapterTitle", "type": "Edm.String", "retrievable": True, "searchable": True, "filterable": True, "sortable": True, "facetable": True},

        {"name": "SectionTitle", "type": "Edm.String", "retrievable": True, "searchable": True, "filterable": True, "sortable": False, "facetable": True},

        {"name": "SubsectionTitle", "type": "Edm.String", "retrievable": True, "searchable": True, "filterable": True, "sortable": True, "facetable": False},

        {"name": "SubsectionText", "type": "Edm.String", "retrievable": True, "searchable": True, "filterable": False, "sortable": False, "facetable": False, "analyzer": "en.microsoft"},

        {"name": "Keywords", "type": "Edm.String", "retrievable": True, "searchable": True, "filterable": False, "sortable": False, "facetable": False, "analyzer": "en.microsoft"}
        ]
    }

def getServiceUrl():
    return 'https://' + serviceName + '.search.windows.net'

def getMethod(servicePath):
    headers = {'Content-type': 'application/json', 'api-key': apiKey}
    r = requests.get(getServiceUrl() + servicePath, headers=headers)
    #print(r.text)
    return r

def postMethod(servicePath, body):
    headers = {'Content-type': 'application/json', 'api-key': apiKey}
    r = requests.post(getServiceUrl() + servicePath, headers=headers, data=body)
    #print(r, r.text)
    return r

def createIndex():
    indexDefinition = json.dumps(getIndexDefinition())  
    servicePath = '/indexes/?api-version=%s' % apiVersion
    r = postMethod(servicePath, indexDefinition)
    #print r.text
    if r.status_code == 201:
       print('Index %s created' % indexName)   
    else:
       print('Failed to create index %s' % indexName)
       exit(1)

def deleteIndex():
    servicePath = '/indexes/%s?api-version=%s&delete' % (indexName, apiVersion)
    headers = {'Content-type': 'application/json', 'api-key': apiKey}
    r = requests.delete(getServiceUrl() + servicePath, headers=headers)
    #print(r.text)

def getIndex():
    servicePath = '/indexes/%s?api-version=%s' % (indexName, apiVersion)
    r = getMethod(servicePath)
    if r.status_code == 200:  
       return True
    else:
       return False

def getDocumentObject():   
    valarry = []
    cnt = 1
    records = pe.iget_records(file_name=inputfile)
    for row in records:
        outdict = {}
        outdict['@search.action'] = 'upload'

        if (row[fields_map[0][0]]):
            outdict['Index'] = str(row['Index'])
            for (in_fld, out_fld) in fields_map:
                outdict[out_fld]  = row[in_fld]
        valarry.append(outdict)
        cnt+=1

    return {'value' : valarry}

def getDocumentObjectByChunk(start, end):   
    valarry = []
    cnt = 1
    records = pe.iget_records(file_name=inputfile)
    for i, row in enumerate(records):
        if start <= i < end:
            outdict = {}
            outdict['@search.action'] = 'upload'

            if (row[fields_map[0][0]]):
                outdict['Index'] = str(row['Index'])
                for (in_fld, out_fld) in fields_map:
                    outdict[out_fld]  = row[in_fld]
            valarry.append(outdict)
            cnt+=1

    return {'value' : valarry}

# Upload content for indexing in one request if content is not too large
def uploadDocuments():
    documents = json.dumps(getDocumentObject())
    servicePath = '/indexes/' + indexName + '/docs/index?api-version=' + apiVersion
    r = postMethod(servicePath, documents)
    if r.status_code == 200:
        print('Success: %s' % r)   
    else:
        print('Failure: %s' % r.text)
        exit(1)

# Upload content for indexing in chunks if content is too large for one request
def uploadDocumentsInChunks(chunksize):
    records = pe.iget_records(file_name=inputfile)
    cnt  = 0
    for row in records:
        cnt += 1

    for chunk in range(cnt/chunksize + 1):
        print('Processing chunk number %d ...' % chunk)
        start = chunk * chunksize
        end   = start + chunksize
        documents = json.dumps(getDocumentObjectByChunk(start, end))
        servicePath = '/indexes/' + indexName + '/docs/index?api-version=' + apiVersion
        r = postMethod(servicePath, documents)
        if r.status_code == 200:
            print('Success: %s' % r)   
        else:
            print('Failure: %s' % r.text)
    return

# Upload content for indexing one document at a time
def uploadDocumentsOneByOne():
    records = pe.iget_records(file_name=inputfile)
    valarry = []
    for i, row in enumerate(records):
        outdict = {}
        outdict['@search.action'] = 'upload'

        if (row[fields_map[0][0]]):
            outdict['Index'] = str(row['Index'])
            for (in_fld, out_fld) in fields_map:
                outdict[out_fld]  = row[in_fld]
            valarry.append(outdict)

        documents = json.dumps({'value' : valarry})
        servicePath = '/indexes/' + indexName + '/docs/index?api-version=' + apiVersion
        r = postMethod(servicePath, documents)
        if r.status_code == 200:
            print('%d Success: %s' % (i,r))   
        else:
            print('%d Failure: %s' % (i, r.text))
            exit(1)

def printDocumentCount():
    servicePath = '/indexes/' + indexName + '/docs/$count?api-version=' + apiVersion   
    getMethod(servicePath)

def sampleQuery(query, ntop=3):
    servicePath = '/indexes/' + indexName + '/docs?api-version=%s&search=%s&$top=%d' % \
        (apiVersion, query, ntop)
    getMethod(servicePath)

if __name__ == '__main__':
    # Create index if it does not exist
    if not getIndex():
        createIndex()    
    else:
        ans = raw_input('Index %s already exists ... Do you want to delete it? [Y/n]' % indexName)
        if ans.lower() == 'y':
            deleteIndex()
            print('Re-creating index %s ...' % indexName)
            createIndex()
        else:
            print('Index %s is not deleted ... New content will be added to existing index' % indexName)

    #getIndex()
    #uploadDocuments()
    uploadDocumentsInChunks(50)
    #uploadDocumentsOneByOne()
    printDocumentCount()
    sampleQuery('child tax credit')