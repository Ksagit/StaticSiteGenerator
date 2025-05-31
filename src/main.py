import os
import shutil
import sys
from page_generator import generate_pages_recursive


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
    public_dir = "./docs"
    content_dir = "./content"
    template_file = "./template.html"

    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        if basepath and not basepath.endswith('/'):
            basepath += '/'
    
    print(f"Using basepath: {basepath}")

    copy_static_assets(static_dir, public_dir)

    if not os.path.exists(content_dir):
        print(f"Error: Content directory not found at {content_dir}")
        return
    
    if not os.path.exists(template_file):
        print(f"Error: Template file not found at {template_file}")
        return

    generate_pages_recursive(content_dir, template_file, public_dir, basepath)

    print("Static site generation complete.")


if __name__ == "__main__":
    main()