from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch(["http://localhost:9200"])
def search_documents(keyword):
    search_body = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["section_header", "subsection_header", "text"],
                "type": "best_fields"
            }
        },
        "highlight": {
            "fields": {
                "section_header": {},
                "subsection_header": {},
                "text": {}
            }
        }
    }

    # Thực hiện tìm kiếm trên Elasticsearch
    result = es.search(index="documents", body=search_body)
    hits = result['hits']['hits']
    search_results = []

    # Dùng để theo dõi các phần đã xử lý
    processed_headers = set()  # Để kiểm tra header đã xử lý
    processed_subheaders = set()  # Để kiểm tra subheader đã xử lý
    processed_paragraphs = set()  # Để kiểm tra paragraph đã xử lý

    # Bước 1: Kiểm tra và trả về các section_header trùng và có text khác
    for hit in hits:
        source = hit['_source']
        highlight = hit.get('highlight', {})

        # Kiểm tra nếu từ khóa có trong section_header và có text khác (cũng có highlight trong text)
        if "section_header" in highlight and "text" in highlight and source.get("section_header") not in processed_headers:
            search_results.append({
                "section_header": source.get("section_header"),
                "subsection_header": source.get("subsection_header"),
                "text": source.get("text"),
                "page_number": source.get("page_number"),
                "start_line": source.get("start_line"),
                "end_line": source.get("end_line")
            })
            processed_headers.add(source.get("section_header"))  # Đánh dấu header đã xử lý

    # Bước 2: Nếu không có section_header trùng hoặc sau khi trả về, tiếp tục kiểm tra subsection_header
    for hit in hits:
        source = hit['_source']
        highlight = hit.get('highlight', {})

        # Nếu từ khóa có trong subsection_header và chưa xử lý trước đó
        if "subsection_header" in highlight and source.get("subsection_header") not in processed_subheaders:
            search_results.append({
                "subsection_header": source.get("subsection_header"),
                "page_number": source.get("page_number")
            })
            processed_subheaders.add(source.get("subsection_header"))  # Đánh dấu subheader đã xử lý

    # Bước 3: Nếu không có header hoặc subheader trùng, kiểm tra text
    for hit in hits:
        source = hit['_source']
        highlight = hit.get('highlight', {})

        # Nếu từ khóa có trong text và chưa xử lý trước đó
        if "text" in highlight and source.get("text") not in processed_paragraphs:
            search_results.append({
                "text": source.get("text"),
                "page_number": source.get("page_number"),
                "start_line": source.get("start_line"),
                "end_line": source.get("end_line")
            })
            processed_paragraphs.add(source.get("text"))  # Đánh dấu paragraph đã xử lý

    return search_results


@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    try:
        results = search_documents(keyword)
        if not results:
            return jsonify({"message": "No documents found with the given keyword."}), 404

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Chạy ứng dụng Flask
if __name__ == '__main__':
    app.run(debug=True)
