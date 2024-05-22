import shutil
import os
from copy_static import copy_static

def main(): 
    source = "/Users/derek/code/staticsitegen/static"
    destination = "/Users/derek/code/staticsitegen/public"
    shutil.rmtree(destination, ignore_errors=True)
    os.mkdir(destination)
    copy_static(source, destination)

if __name__ == "__main__":
    main()
