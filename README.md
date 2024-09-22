## Draf pipelines
With the simple idea of using the directory structure of a PDF file, I get the tree of section and traversed each section with the corresponding chunk text information, then inserted it into ES.
### 1. Deploy ElasticSeach: 
```docker-compose up -d```
### 2. Extract and insert information into ES:
```python main.py```
### 3. Implement API Search: 
```python search.py```
