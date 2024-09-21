import fitz  # PyMuPDF
from extract.document_outline import build_tree_outline, extract_paragraphs_with_metadata

if __name__ == '__main__':
    pdf_path = "s3-userguide.pdf"
    doc = fitz.open(pdf_path)
    tree_outline = build_tree_outline(doc.get_toc())

    # Giả sử doc là file PDF đã mở và tree_outline đã được xây dựng
    for chunk in extract_paragraphs_with_metadata(doc, tree_outline):
        # Xử lý từng chunk ngay khi nó được yield
        print(f"Processing chunk from Page {chunk['page_number']} Block {chunk['block_number']}")
        print(f"Section: {chunk['section_header']}, Subsection: {chunk['subsection_header']}")
        print(f"Start Line: {chunk['start_line']}, End Line: {chunk['end_line']}")
        print(f"Text: {chunk['text']}\n")



