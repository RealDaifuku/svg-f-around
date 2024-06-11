import os
from svgpathtools import svg2paths

def svg_to_gcode(svg_file, gcode_file):
    # Parse SVG paths from the file
    paths, attributes = svg2paths(svg_file)

    # Open the G-code file for writing
    with open(gcode_file, 'w') as f:
        # Write G-code header
        f.write("G21 ; Set units to millimeters\n")
        f.write("G90 ; Use absolute coordinates\n")
        f.write("G1 F1000 ; Set feed rate\n")
        
        # Process each path in the SVG file
        for path in paths:
            # Iterate through each segment of the path
            for segment in path:
                start = segment.start
                end = segment.end
                # Move to the start point of the segment
                f.write(f"G0 X{start.real:.3f} Y{start.imag:.3f}\n")
                # Draw the segment
                f.write(f"G1 X{end.real:.3f} Y{end.imag:.3f}\n")
        
        # Write G-code footer
        f.write("M2 ; End of program\n")

def convert_all_svgs_to_gcode(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".svg"):
            svg_file = os.path.join(directory, filename)
            gcode_file = os.path.join(directory, filename.replace('.svg', '.gcode'))
            svg_to_gcode(svg_file, gcode_file)
            print(f"Converted {svg_file} to {gcode_file}")

# Example usage
convert_all_svgs_to_gcode('.')
