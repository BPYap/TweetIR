# TweetIR

### Environment Setup
1. Create a virtual environment using `python3 -m virtualenv env`
2. Activate the virtual environment using `env\scripts\activate` (Windows) or `source env/bin/activate` (Ubuntu)
3. Install local dependencies using `python setup.py install`
4. Install external dependencies using `pip install -r requirements.txt`
5. Replace the url value in `config.json` with elasticsearch server url (Host supported: [Bonsai](https://bonsai.io/) & [Searchly](http://www.searchly.com/)) 

### Indexing Using Searchly Elasticsearch server
1. Create a Searchly account with free plan at https://dashboard.searchly.com/users/sign_up
2. Change directory to `/indexer` using `cd indexer`
3. Run indexer using `python create_index.py` (this will take a while)

### Hosting Web Interface Locally
1. Activate virtual environment
2. Change directory into `web_interface` using `cd web_interface`
3. Start local host server (http://127.0.0.1:8000) using `python manage.py runserver`

### Technology Stack
- Django
- Materialize CSS
- Elasticsearch
- TwitterScraper
- XGBoost

### Video Demo
[![](http://img.youtube.com/vi/QumGbXd1au8/0.jpg)](http://www.youtube.com/watch?v=QumGbXd1au8 "Video Demo")

