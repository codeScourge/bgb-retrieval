# bgb-retrieval
An advanced pipeline for performing RAG operations on the german BGB

### steps for running
- pip install -r requirements.txt
- set your OPENAI_API_KEy
- export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

### files
- data.py parses a xml file from https://www.gesetze-im-internet.de and saves them in JSON format
- index.py creates a vector-database from the JSON data
- retrieval retrieves most fitting data using similarity search of the query and the title, as well as reranks the results using a Cross-Encoder based on the text-content itself
