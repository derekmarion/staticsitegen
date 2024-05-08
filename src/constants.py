import re

BLOCK_TYPE_PARAGRAPH = "paragraph"
BLOCK_TYPE_HEADING = "heading"
BLOCK_TYPE_CODE = "code"
BLOCK_TYPE_QUOTE = "quote"
BLOCK_TYPE_UNORDERED_LIST = "ul"
BLOCK_TYPE_ORDERED_LIST = "ol"

# Pre-compile the regex pattern for headings for efficiency
heading_pattern = re.compile(r"#{1,6}\s")
