def build_tree_outline(toc):
    tree = {}
    stack = [tree]
    for idx, item in enumerate(toc):
        level, title, start_page = item
        if idx < len(toc) - 1:
            next_start_page = toc[idx + 1][2]
        else:
            next_start_page = start_page
        end_page = next_start_page - 1 if next_start_page > start_page else start_page
        while len(stack) > level:
            stack.pop()
        current_level = stack[-1]
        new_item = {
            "title": title,
            "start_page": start_page,
            "end_page": end_page,
            "subsections": {},
        }
        current_level[title] = new_item
        stack.append(new_item["subsections"])
    return tree


def extract_paragraphs_with_metadata(doc, tree_outline):
    def traverse_and_extract(node, section_header=None, subsection_header=None):
        start_page = node.get("start_page")
        end_page = node.get("end_page")

        if start_page is not None and end_page is not None:
            for page_num in range(start_page, end_page + 1):
                page = doc.load_page(page_num - 1)
                blocks = page.get_text("blocks")
                line_counter = 1

                # Mỗi block sẽ là một đoạn văn
                for block_num, block in enumerate(blocks, start=1):
                    block_text = block[4]

                    block_lines = block_text.splitlines()
                    start_line = line_counter
                    end_line = start_line + len(block_lines) - 1

                    chunk = {
                        "block_number": block_num,
                        "section_header": section_header,
                        "subsection_header": subsection_header,
                        "text": block_text,
                        "page_number": page_num,
                        "start_line": start_line,
                        "end_line": end_line
                    }

                    yield chunk
                    line_counter = end_line + 1

        subsections = node.get("subsections", {})
        for subsection_title, subsection_node in subsections.items():
            yield from traverse_and_extract(subsection_node, section_header=node["title"], subsection_header=subsection_title)

    for section_title, section_node in tree_outline.items():
        yield from traverse_and_extract(section_node, section_header=section_title)






