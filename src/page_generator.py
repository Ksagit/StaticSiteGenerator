import os
from markdown_converter import extract_title, markdown_to_html_node


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path} with basepath {basepath}")

    with open(from_path, 'r') as f:
        markdown_content = f.read()

    with open(template_path, 'r') as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    page_html_content = html_node.to_html()

    page_title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", page_title)
    final_html = final_html.replace("{{ Content }}", page_html_content)

    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, 'w') as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    print(f"Recursively generating pages from {dir_path_content} to {dest_dir_path} with basepath {basepath}")

    if not os.path.exists(dir_path_content):
        raise FileNotFoundError(f"Content directory not found: {dir_path_content}")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")

    os.makedirs(dest_dir_path, exist_ok=True)

    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(item_path):
            if item.endswith(".md"):
                file_name_html = item.replace(".md", ".html")
                dest_file_path = os.path.join(dest_dir_path, file_name_html)
                # Pass basepath to generate_page
                generate_page(item_path, template_path, dest_file_path, basepath)
            else:
                print(f"  Skipping non-markdown file: {item_path}")
        elif os.path.isdir(item_path):
            new_dest_dir_path = os.path.join(dest_dir_path, item)
            # Pass basepath to recursive call
            generate_pages_recursive(item_path, template_path, new_dest_dir_path, basepath)