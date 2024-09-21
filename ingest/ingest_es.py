from elasticsearch import Elasticsearch
from loguru import logger
from extract.document_outline import extract_paragraphs_with_metadata

es = Elasticsearch("http://localhost:9200",
                   headers={"Content-Type": "application/json"}
                   )

# Define the mapping for your index
index_name = "documents"

mapping = {
    "mappings": {
        "properties": {
            "section_header": {"type": "text"},
            "subsection_header": {"type": "text"},
            "text": {"type": "text"},
            "page_number": {"type": "integer"},
            "block_number": {"type": "integer"},
            "start_line": {"type": "integer"},
            "end_line": {"type": "integer"}
        }
    }
}

es.indices.create(index=index_name, body=mapping, ignore=400)  # 400 here means ignore if the index already exists

def insert_into_elasticsearch(doc, tree_outline):
    # Iterate over the extracted paragraphs with metadata
    for chunk in extract_paragraphs_with_metadata(doc, tree_outline):
        logger.info(f"Inserting chunk from Page {chunk['page_number']} Block {chunk['block_number']}")
        es.index(index=index_name, body=chunk)


