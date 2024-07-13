import xml.etree.ElementTree as ET
import os
from pathlib import Path

def parse_node(node, depth=0):
    """
    Recursive function to parse each node and convert to markdown format.
    """
    markdown = ''
    # Create markdown line for this node, indenting based on depth
    text = node.get('TEXT', '')
    markdown += f"{'  ' * depth}- {text}\n"

    # Handle links if present
    link = node.get('LINK')
    if link:
        markdown += f"{'  ' * (depth + 1)}[Link]({link})\n"

    # Process child nodes recursively
    for child in node.findall('node'):
        markdown += parse_node(child, depth + 1)

    return markdown

def mm_to_markdown(file_path):
    """
    Reads an .mm file and converts its XML content to Markdown format.
    """
    try:
        # Parse the XML from the file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Assume that the root <map> element contains a single <node> child
        if root.tag == 'map':
            main_node = root.find('node')
            if main_node is not None:
                return parse_node(main_node)
        return "Invalid XML structure"
    except Exception as e:
        return f"An error occurred: {e}"

def save_markdown(markdown, output_path):
    """
    Save the markdown text to a file.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)

def process_batch(input_dir):
    """
    Process a batch of .mm files and convert them to markdown.
    """
    input_path = Path(input_dir)
    for mm_file in input_path.glob('*.mm'):
        markdown = mm_to_markdown(mm_file)
        output_file = mm_file.with_suffix('.md')
        save_markdown(markdown, output_file)
        print(f"Converted: {mm_file} -> {output_file}")

# Directory path to your .mm files
input_directory = r'C:\Users\mypc\Desktop\CodeCamp'

# Process the batch of .mm files
process_batch(input_directory)
