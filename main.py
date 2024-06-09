import xml.etree.ElementTree as ET

def separate_svg_layers(svg_file):
    # Parse the SVG file
    tree = ET.parse(svg_file)
    root = tree.getroot()

    # Create a dictionary to hold layers
    layers = {}

    # Iterate through all elements
    for elem in root.iter():
        # Check if the element has an ID
        if 'id' in elem.attrib:
            # Get the ID
            elem_id = elem.attrib['id']
            
            # Check if the ID already exists as a layer
            if elem_id not in layers:
                # If not, create a new layer
                layers[elem_id] = ET.Element('svg', attrib={'xmlns': 'http://www.w3.org/2000/svg'})
            
            # Append the element to the respective layer
            layers[elem_id].append(elem)

    # Create a new SVG tree for each layer
    for layer_id, layer_root in layers.items():
        # Write the layer to a separate SVG file
        layer_tree = ET.ElementTree(layer_root)
        layer_tree.write(f'{layer_id}.svg', encoding='utf-8', xml_declaration=True)

# Example usage
separate_svg_layers('example.svg')
