import re

BLOCK_TYPE_PARAGRAPH = "paragraph"
BLOCK_TYPE_HEADING = "heading"
BLOCK_TYPE_CODE = "code"
BLOCK_TYPE_QUOTE = "quote"
BLOCK_TYPE_UNORDERED_LIST = "ul"
BLOCK_TYPE_ORDERED_LIST = "ol"

TAG_TYPE_PARAGRAPH = "p"
TAG_TYPE_HEADING = "h"
TAG_TYPE_CODE = "code"
TAG_TYPE_PREFORMATTED_TEXT = "pre"
TAG_TYPE_QUOTE = "blockquote"
TAG_TYPE_UNORDERED_LIST = "ul"
TAG_TYPE_ORDERED_LIST = "ol"
TAG_TYPE_LIST_ITEM = "li"
TAG_TYPE_DIV = "div"
TAG_TYPE_BOLD = "b"
TAG_TYPE_ITALIC = "i"

# Pre-compile the regex pattern for headings for efficiency. Implemented in textnode.py
heading_pattern = re.compile(r"#{1,6}\s")
