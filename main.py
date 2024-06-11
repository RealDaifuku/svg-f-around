import xml.etree.ElementTree as ET
import os
from svgpathtools import svg2paths

def separate_svg_layers(svg_file):
    tree = ET.parse(svg_file)
    root = tree.getroot()
    layers = {}

    for elem in root.iter():
        if 'id' in elem.attrib:
            elem_id = elem.attrib['id']
            
            if elem_id not in layers:
                layers[elem_id] = ET.Element('svg', attrib={'xmlns': 'http://www.w3.org/2000/svg'})
            
            layers[elem_id].append(elem)

    for layer_id, layer_root in layers.items():
        layer_tree = ET.ElementTree(layer_root)
        layer_tree.write(f'generated_files/{layer_id}.svg', encoding='utf-8', xml_declaration=True)

def svg_to_gcode(svg_file, gcode_file):
    paths, attributes = svg2paths(svg_file)

    with open(gcode_file, 'w') as f:
        f.write("G21 ; Set units to millimeters\n")
        f.write("G90 ; Use absolute coordinates\n")
        f.write("G1 F1000 ; Set feed rate\n")
        
        for path in paths:
            for segment in path:
                start = segment.start
                end = segment.end
                f.write(f"G0 X{start.real:.3f} Y{start.imag:.3f}\n")
                f.write(f"G1 X{end.real:.3f} Y{end.imag:.3f}\n")
        
        f.write("M2 ; End of program\n")

def convert_all_svgs_to_gcode(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".svg"):
            svg_file = os.path.join(directory, filename)
            gcode_file = os.path.join(directory, filename.replace('.svg', '.gcode'))
            svg_to_gcode(svg_file, gcode_file)
            print(f"Converted {svg_file} to {gcode_file}")

def create_folder(directory):
    try:
        os.mkdir(directory)
        print(f"Directory '{directory}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory}' already exists.")

folder_name = "generated_files"
create_folder(folder_name)
separate_svg_layers('input.svg')
convert_all_svgs_to_gcode('./generated_files/')





