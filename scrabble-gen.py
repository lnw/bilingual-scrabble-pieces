#!/usr/bin/env python3

import os
import signal
import sys
import math
import subprocess
from argparse import ArgumentParser


def parseCommandline():
    parser = ArgumentParser(prog="scrabble-gen.py", description="nothing yet", add_help=True)
    parser.add_argument("--lang1", help="foo", dest="lang1", action="store", type=str, required=True)
    parser.add_argument("--lang2", help="foo", dest="lang2", action="store", type=str, required=True)
    argparse = parser.parse_args()
    return argparse


def read_letters(lang):
    path = "letter-distros/" + str(lang)
    letters = []
    with open(path, 'r') as f:
        for line in f:
            letters.append(line.split())
    return letters


def get_svg_header(width, height):
    s = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="{0}mm"
   height="{1}mm"
   viewBox="0 0 {0} {1}"
   version="1.1"
   id="svg8"
   inkscape:version="0.92.4 (5da689c313, 2019-01-14)"
   sodipodi:docname="drawing.svg">
  <defs
     id="defs2" />
  <sodipodi:namedview
     id="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="2"
     inkscape:cx="-143.47209"
     inkscape:cy="424.77451"
     inkscape:document-units="mm"
     inkscape:current-layer="layer1"
     showgrid="false"
     inkscape:window-width="1920"
     inkscape:window-height="995"
     inkscape:window-x="0"
     inkscape:window-y="24"
     inkscape:window-maximized="1" />
  <metadata
     id="metadata5">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title />
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1">\n""".format(width, height)
    return s


def get_svg_footer():
    s = """ </g>
</svg>"""
    return s


def single_piece(centrex, centrey, cut, frame, letter, letter_font_size, letter_x_offset, value, idno):
    sidelength = 15.0
    sidelength_frame = 12.0
    rad_out = 1.5
    rad_in = 0.5 #rad_out - (sidelength - sidelength_frame)/2.0
    val_font_size = 3.8
    string = ""
    if(cut):
        string += '<path\n'
        string += '   sodipodi:nodetypes="ccccc"\n'
        string += '   id="path' + str(idno) + '"\n'
        string += '   inkscape:label="part"\n'
        string += '   style="fill:none;stroke:#ff0000;stroke-width:0.01;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"\n'
        string += '   d="M {:.1f},{:.1f} a {:.1f},{:.1f} 0 0 1 {:.1f},{:.1f} h {:.1f} a {:.1f},{:.1f} 0 0 1 {:.1f},{:.1f} v {:.1f} a {:.1f},{:.1f} 0 0 1 {:.1f},{:.1f} h {:.1f} a {:.1f},{:.1f} 0 0 1 {:.1f},{:.1f} Z"\n'.format(centrex-sidelength/2.0, centrey-sidelength/2.0+rad_out, rad_out, rad_out, rad_out, -rad_out, sidelength-2*rad_out, rad_out, rad_out, rad_out, rad_out, sidelength-2*rad_out ,rad_out, rad_out, -rad_out, rad_out, -sidelength+2*rad_out, rad_out, rad_out, -rad_out, -rad_out)
        string += '   inkscape:connector-curvature="0" />\n'
    if(frame):
        string += '<path\n'
        string += '   sodipodi:nodetypes="cccccsscc"\n'
        string += '   id="path' + str(idno + 1) + '"\n'
        string += '   inkscape:label="part"\n'
        string += '   style="fill:none;stroke:#000000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"\n'
        string += '   d="M {:.1f},{:.1f} a {:.1f},{:.1f} 0 0 1 {:.1f},{:.1f} h {:.1f} a {:.1f},{:.1f} 0 0 1 {:.1f},{:.1f} v {:.1f} a {:.1f},{:.1f} 0 0 1 {:.1f},{:.1f} h {:.1f} a {:.1f},{:.1f} 0 0 1 {:.1f},{:.1f} Z"\n'.format(centrex-sidelength_frame/2.0, centrey-sidelength_frame/2.0+rad_in, rad_in, rad_in, rad_in, -rad_in, sidelength_frame-2*rad_in, rad_in, rad_in, rad_in, rad_in, sidelength_frame-2*rad_in ,rad_in, rad_in, -rad_in, rad_in, -sidelength_frame+2*rad_in, rad_in, rad_in, -rad_in, -rad_in)
        string += '   inkscape:connector-curvature="0"/>\n'
    string += '<text\n'
    string += '   xml:space="preserve"\n'
    string += """   style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:{:.1f}px;line-height:1.25;font-family:sans-serif;-inkscape-font-specification:'sans-serif, Normal';font-variant-ligatures:normal;font-variant-caps:normal;font-variant-numeric:normal;font-feature-settings:normal;text-align:start;letter-spacing:0px;word-spacing:0px;writing-mode:lr-tb;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0.26458332"\n""".format(letter_font_size)
    string += '   text-anchor="middle"\n'
    string += '   x="{:.1f}"\n'.format(centrex + letter_x_offset)
    string += '   y="{:.1f}"\n'.format(centrey + 3.5)
    string += '   id="text866"><tspan\n'
    string += '     sodipodi:role="line"\n'
    string += '     id="tspan864"\n'
    string += '     x="0"\n'
    string += '     y="0"\n'
    string += """     style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:{:.1f}px;font-family:sans-serif;-inkscape-font-specification:'sans-serif, Normal';font-variant-ligatures:normal;font-variant-caps:normal;font-variant-numeric:normal;font-feature-settings:normal;text-align:start;writing-mode:lr-tb;stroke-width:0.26458332">{}</tspan></text>\n""".format(letter_font_size, letter)
    string += '<text\n'
    string += '   xml:space="preserve"\n'
    string += """   style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:{:.1f}px;line-height:1.25;font-family:sans-serif;-inkscape-font-specification:'sans-serif, Normal';font-variant-ligatures:normal;font-variant-caps:normal;font-variant-numeric:normal;font-feature-settings:normal;text-align:start;letter-spacing:0px;word-spacing:0px;writing-mode:lr-tb;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0.26458332"\n""".format(val_font_size)
    string += '   text-anchor="end"\n'
    string += '   x="{:.1f}"\n'.format(centrex + sidelength_frame/2.0 - 0.5)
    string += '   y="{:.1f}"\n'.format(centrey + sidelength_frame/2.0 - 0.8)
    string += '   id="text870"><tspan\n'
    string += '     sodipodi:role="line"\n'
    string += '     id="tspan868"\n'
    string += '     x="0"\n'
    string += '     y="0"\n'
    string += """     style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:{:.1f}px;font-family:sans-serif;-inkscape-font-specification:'sans-serif, Normal';font-variant-ligatures:normal;font-variant-caps:normal;font-variant-numeric:normal;font-feature-settings:normal;text-align:start;writing-mode:lr-tb;stroke-width:0.26458332">{}</tspan></text>\n""".format(val_font_size, value)
    return string


def print_one_side(pieces, outfile, frame, cut, lefttoright):
    output_str = ''
    print(pieces)
    canvas_width = 200
    canvas_height = 200
    output_str += get_svg_header(canvas_width, canvas_height)
    x_increment = 16
    y_increment = 16
    if (lefttoright):
        x_start_pos = x_increment/2.0
    else:
        x_increment = -x_increment
        x_start_pos = canvas_width + x_increment/2.0
    x = x_start_pos
    y = y_increment/2.0
    letter_counter = 0
    for entry in pieces:
        [value, number, letter] = entry
        if (letter == 'blank'):
            value = ''
            letter = ''
        if (letter == 'null'):
            let_size = 4.5
            let_x_offset = 0.0
        else:
            let_size = 10.2
            let_x_offset = -0.5
        for i in range(0, int(number)):
            letter_counter += 1
            output_str += single_piece(x, y, cut, frame, letter=letter, letter_font_size=let_size, letter_x_offset = let_x_offset, value=value, idno=2)
            x += x_increment
            if (letter_counter % 10 == 0):
                x = x_start_pos
                y += y_increment
    output_str += get_svg_footer()
    with open(outfile, 'w') as f:
        f.write(output_str)

def number_of_pieces(pieces):
    accumulator = 0
    for type in pieces:
        accumulator += int(type[1])
    return accumulator

def pad_pieces(pieces1, pieces2):
    no1 = number_of_pieces(pieces1)
    no2 = number_of_pieces(pieces2)
    if (no1 > no2):
        pieces2.append(['', no1 - no2, 'null'])
    elif (no2 > no1):
        pieces1.append(['', no2 - no1, 'null'])
    

def main():
    # signal.signal(signal.SIGINT, signal_handler)
    args = parseCommandline()
    # print(args)
    pieces_l1 = read_letters(args.lang1)
    pieces_l2 = read_letters(args.lang2)
    pad_pieces(pieces_l1, pieces_l2)
    print_one_side(pieces_l1, 'side1.svg', frame=True, cut=False, lefttoright = True)
    print_one_side(pieces_l2, 'side2.svg', frame=False, cut=True, lefttoright = False)
    process = subprocess.Popen(['inkscape', 'side1.svg', '--export-text-to-path', '--export-pdf=side1.pdf'],
    # process = subprocess.Popen(['inkscape', 'side1.svg', '--export-text-to-path', '--export-plain-svg=lala1.svg'],
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout)
    print(stderr)
    process = subprocess.Popen(['inkscape', 'side2.svg', '--export-text-to-path', '--export-pdf=side2.pdf'],
    # process = subprocess.Popen(['inkscape', 'side2.svg', '--export-text-to-path', '--export-plain-svg=lala2.svg'],
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout)
    print(stderr)


if __name__ == "__main__":
    main()

