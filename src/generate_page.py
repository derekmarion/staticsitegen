import re
from helpers import markdown_to_html_node

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
    with open(dest_path, 'w') as f:
        f.write(template)
