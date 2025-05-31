import os
import shutil
from page_generator import generate_page


def copy_static_assets(source_dir, dest_dir):
    print(f"Cleaning and copying static assets from {source_dir} to {dest_dir}")

    if os.path.exists(dest_dir):
        print(f"  Deleting existing directory: {dest_dir}")
        shutil.rmtree(dest_dir)
    print(f"  Creating new directory: {dest_dir}")
    os.mkdir(dest_dir)

    for item in os.listdir(source_dir):
        source_item_path = os.path.join(source_dir, item)
        dest_item_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_item_path):
            print(f"  Copying file: {source_item_path} to {dest_item_path}")
            shutil.copy(source_item_path, dest_item_path)
        elif os.path.isdir(source_item_path):
            print(f"  Entering directory: {source_item_path}")
            copy_static_assets(source_item_path, dest_item_path)


def main():
    print("Starting static site generation...")

    static_dir = "./static"
    public_dir = "./public"
    content_dir = "./content"
    template_file = "./template.html"

    copy_static_assets(static_dir, public_dir)

    markdown_file_path = os.path.join(content_dir, "index.md")
    output_html_path = os.path.join(public_dir, "index.html")

    if not os.path.exists(markdown_file_path):
        print(f"Error: Markdown file not found at {markdown_file_path}")
        print("Please ensure you have a 'content/index.md' file in your project root.")
        return
    
    if not os.path.exists(template_file):
        print(f"Error: Template file not found at {template_file}")
        print("Please ensure you have a 'template.html' file in your project root.")
        return

    generate_page(markdown_file_path, template_file, output_html_path)

    print("Static site generation complete.")


if __name__ == "__main__":
    main()