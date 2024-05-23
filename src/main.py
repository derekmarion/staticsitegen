import shutil
import os
from copy_static import copy_static
from generate_page import generate_pages_recursive

def main(): 
    # Copy static files to public folder
    source = "/Users/derek/code/staticsitegen/static"
    destination = "/Users/derek/code/staticsitegen/public"
    shutil.rmtree(destination, ignore_errors=True)
    os.mkdir(destination)
    copy_static(source, destination)

    # Generate HTML page from MD file to public folder
    from_path = "/Users/derek/code/staticsitegen/content/"
    dest_path = "/Users/derek/code/staticsitegen/public/"
    template_path = "/Users/derek/code/staticsitegen/template.html"
    generate_pages_recursive(from_path, template_path, dest_path)

if __name__ == "__main__":
    main()
