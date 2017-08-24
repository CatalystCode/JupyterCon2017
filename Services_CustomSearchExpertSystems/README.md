
# Custom Search 

> Sample custom search project using Azure Search and the US Tax Code.

> Python scripts and Jupyter notebooks that allow you to quickly and iteratively customize, 
improve and measure your custom search experience.

## Description
Querying specific content areas quickly and easily is a common services sector need. Fast traversal of specialized publications, customer support knowledge bases or document repositories allows service companies to deliver their particular service efficiently and effectively. Simple FAQs don’t cover enough ground, and a string search isn’t effective or efficient for those not familiar with the domain or the document set. Instead, these companies can deliver a custom search experience that saves their clients time and provides them better service through a question and answer format.  In this project, we leveraged Azure Search and Cognitive Services and we share our custom code for iterative testing, measurement and indexer redeployment. In our solution, the customized search engine will form the foundation for delivering a question and answer experience in a specific domain area.

## End-to-End Example Provided in Jupyter Notebooks
* Collect, pre-process, and augment content with keyphrases
* Create an Azure Search index
* Query the index and retrieve results interactively and/or in batch

## Getting Started

1. Read the [Real Life Code Story](https://www.microsoft.com/reallifecode/), "[Developing a Custom Search Engine for an Expert Chat System.](https://www.microsoft.com/reallifecode/)"
2. Review the [Azure Search service features](https://azure.microsoft.com/en-us/services/search/).
3. Get a [free trial subscriptions to Azure Search.](https://azure.microsoft.com/en-us/free/)
4. Copy your Azure Search name and Key. 
5. Review the [sample](https://github.com/CatalystCode/CustomSearch/tree/master/sample)
 search index input and enriched input in the sample folder to understand content.
6. Try the sample Jupyter notebooks for an overview of the end-2-end process for content extraction, augmentation with keyphrases, indexing and retrieval.
	* Step 1: Content and keyphrase extraction: [1-content_extraction.ipynb](https://github.com/CatalystCode/CustomSearch/blob/master/JupyterNotebooks/1-content_extraction.ipynb)
	* Step 2: Index creation: [2-content_indexing.ipynb](https://github.com/CatalystCode/CustomSearch/blob/master/JupyterNotebooks/2-content_indexing.ipynb)
	* Step 3: Interactive and batch search queries: [3-azure_search_query.ipynb](https://github.com/CatalystCode/CustomSearch/blob/master/JupyterNotebooks/3-azure_search_query.ipynb)
7. A command-line version of the scripts is available under the Python folder.
	* Run the [azsearch_mgmt.py script](https://github.com/CatalystCode/CustomSearch/blob/master/Python/azsearch_mgmt.py), using your Azure Search name, key and index name of your choice to create a search index.
	* Run the [azsearch_query.py script](https://github.com/CatalystCode/CustomSearch/blob/master/Python/azsearch_query.py) to interactively query your new search index and see results.
	* Run the [azsearch_queryall.py script](https://github.com/CatalystCode/CustomSearch/blob/master/Python/azsearch_queryall.py) to batch query your new search index and evaluate the results.
	* Run the [keyphrase_extract.py script](https://github.com/CatalystCode/CustomSearch/blob/master/Python/keyphrase_extract.py) to experiment with various keyphrase extraction algorithms to enrich the search index metadata.  Note this script is Python 2.7 only.

 

