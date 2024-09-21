import fitz

from extract.document_outline import build_tree_outline
from ingest.ingest_es import insert_into_elasticsearch

if __name__ == '__main__':
    pdf_path = "s3-userguide.pdf"
    doc = fitz.open(pdf_path)
    tree_outline = build_tree_outline(doc.get_toc())
    insert_into_elasticsearch(doc, tree_outline)


