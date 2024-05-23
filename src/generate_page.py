import re
from helpers import markdown_to_html_node
import os


def extract_title(markdown: str) -> str:
    return re.findall(r"#{1}\s(.*)\n", markdown)


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown source and template files into variables
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()

    # Convert MD to HTML and replace heading and content of template
    html_node = markdown_to_html_node(markdown)
    content = html_node.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title[0])
    template = template.replace("{{ Content }}", content)

    # Write HTML to destination, checking if directories exists
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    # verify source dir exists
    if not os.path.exists(dir_path_content):
        raise ValueError("Source directory does not exist")
    for item in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, item)
        if os.path.isfile(full_path):
            # Generate page from source dir to destination, this is the base case
            dest_item = item[:-2] + "html" # Change file extension
            dest_full_path = os.path.join(dest_dir_path, dest_item)
            generate_page(full_path, template_path, dest_full_path)
        else:
            # If item is a folder, create it at destination
            new_destination_folder = os.path.join(dest_dir_path, item)
            os.mkdir(new_destination_folder)
            # Make recursive call on folder item with dest folder you just created
            generate_pages_recursive(full_path, template_path, new_destination_folder)