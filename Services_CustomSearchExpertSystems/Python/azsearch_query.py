"""
Python code to query Azure Search interactively

Run this script in the 'code' directory:
    python azsearch_query.py

See Azure Search REST API docs for more info:
    https://docs.microsoft.com/en-us/rest/api/searchservice/index

"""

import requests
import json
import os

# This is the service you've already created in Azure Portal
serviceName = 'your_azure_search_service_name'

# This is the index you've already created in Azure Portal or via the azsearch_mgmt.py script
indexName = 'your_index_name_to_use'

# Set your service API key, either via an environment variable or enter it below
#apiKey = os.getenv('SEARCH_KEY_DEV', '')
apiKey = 'your_azure_search_service_api_key'
apiVersion = '2016-09-01'

# Retrieval options to alter the query results
SEARCHFIELDS = None                            # use all searchable fields for retrieval
#SEARCHFIELDS = 'Keywords, SubsectionText'     # use selected fields only for retrieval
FUZZY = False                                  # enable fuzzy search (check API for details)
NTOP  = 5                                      # uumber of results to return


def getServiceUrl():
    return 'https://' + serviceName + '.search.windows.net'

def getMethod(servicePath):
    headers = {'Content-type': 'application/json', 'api-key': apiKey}
    r = requests.get(getServiceUrl() + servicePath, headers=headers)
    #print(r, r.text)
    return r

def postMethod(servicePath, body):
    headers = {'Content-type': 'application/json', 'api-key': apiKey}
    r = requests.post(getServiceUrl() + servicePath, headers=headers, data=body)
    #print(r, r.text)
    return r

def submitQuery(query, fields=None, ntop=10):
    servicePath = '/indexes/' + indexName + '/docs?api-version=%s&search=%s&$top=%d' % \
        (apiVersion, query, ntop)
    if fields != None:
        servicePath += '&searchFields=%s' % fields
    if FUZZY:
        servicePath += '&queryType=full'
    r = getMethod(servicePath)
    if r.status_code != 200:
        print('Failed to retrieve search results')
        print(r, r.text)
        return
    docs = json.loads(r.text)['value']
    print('Number of search results = %d\n' % len(docs))
    for i, doc in enumerate(docs):
        print('Results# %d' % (i+1))
        print('Chapter title   : %s' % doc['ChapterTitle'].encode('utf8'))
        print('Section title   : %s' % doc['SectionTitle'].encode('utf8'))
        print('Subsection title: %s' % doc['SubsectionTitle'].encode('utf8'))
        print('%s\n' % doc['SubsectionText'].encode('utf8'))


#####################################################################
# Azure Search interactive query - command-line interface
# Retrieve Azure Search documents via an interactive query
# Fields: Index	File	ChapterTitle	SectionTitle	SubsectionTitle		SubsectionText	Keywords
#####################################################################
if __name__ == '__main__':
    while True:
        print
        print "Hit enter with no input to quit."
        query = raw_input("Query: ")
        if query == '':
            exit(0)

        # Submit query to Azure Search and retrieve results
        #searchFields = None
        searchFields = SEARCHFIELDS
        submitQuery(query, fields=searchFields, ntop=NTOP)