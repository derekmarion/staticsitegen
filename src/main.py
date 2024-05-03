from textnode import TextNode
from htmlnode import HTMLNode


def main():
    textnode = TextNode("This is a text node", "bold", "https://example.com")
    print(textnode)

    htmlnode = HTMLNode("a", "this is a link", "children", {"href": "https://example.com"})
    print(htmlnode)


if __name__ == "__main__":
    main()
