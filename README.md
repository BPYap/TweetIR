# CZ4034-Information Retrieval Assignment

### Environment Setup
1. Create a virtual environment using `python3 -m virtualenv env`
2. Activate the virtual environment using `env\scripts\activate` (Windows) or `source env/bin/activate` (Ubuntu)
3. Install dependencies using `pip install -r requirements.txt`

### Hosting Web Interface Locally
1. Activate virtual environment
2. Change directory into `web_interface`
3. Start local host server (http://127.0.0.1:8000) using `python manage.py runserver`

### Questions Checklist
| No. |                                                                                                  Questions                                                                                                 |   Status         |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------:|
| 1.1 | How you crawled the corpus (e.g., source, keywords, API, library) and stored them (e.g., whether a record corresponds to a file or a line, meta information like publication date, author name, record ID) |:heavy_check_mark:|
| 1.2 | What kind of information users might like to retrieve from your crawled corpus (i.e., applications), with example queries                                                                                  |:heavy_check_mark:|
| 1.3 | The numbers of records, words, and types (i.e., unique words) in the corpus                                                                                                                                |:heavy_check_mark:|
| 2.1 | Build a simple Web interface for the search engine (e.g., Google)                                                                                                                                          ||
| 2.2 | A simple UI for crawling and incremental indexing of new data would be a bonus (but not compulsory)                                                                                                        ||
| 2.3 | Write five queries, get their results, and measure the speed of the querying                                                                                                                               ||
| 3.1 | Interactive search (e.g., refine search results based on users’ relevance feedback)                                                                                                                        ||
| 3.2 | Improve search results by integrating machine learning or data mining techniques (e.g., classification or cluster techniques)                                                                              ||
| 3.3 | Go beyond text-based search (e.g., implement image retrieval or multimedia retrieval)                                                                                                                      ||
| 3.4 | Exploit geo-spatial data (i.e., map information) to refine query results/improve presentation/visualization                                                                                                ||
| 3.5 | Others (brainstorm with your group members!!)                                                                                                                                                              ||
| 4.1 | Motivate the choice of your classification approach in relation with the state of the art                                                                                                                  ||
| 4.2 | Discuss whether you had to preprocess data and why                                                                                                                                                         ||
| 4.3 | Build an evaluation dataset by manually labeling 10% of the collected data (at least 1,000 records) with an inter-annotator agreement of at least 80%                                                      ||
| 4.4 | Provide evaluation metrics such as precision, recall, and F-measure and discuss results                                                                                                                    ||
| 4.5 | Discuss performance metrics, e.g., records classified per second, and scalability of the system                                                                                                            ||
| 4.6 | A simple UI for visualizing classified data would be a bonus (but not compulsory)                                                                                                                          ||
| 5.1 | Ensemble classification (e.g., leverage on multiple classification approaches)                                                                                                                             ||
| 5.2 | Cognitive classification (e.g., use brain-inspired algorithms)                                                                                                                                             ||
| 5.3 | Multi-faceted classification (e.g., take into account multiple aspects of data)                                                                                                                            ||    
