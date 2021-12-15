#!/usr/bin/python3

import re
import subprocess
from pathlib import Path
from shutil import copyfile

INKSCAPE_EXE = "inkscape"
INKSCAPE_NAME = "Inkscape"
SOURCE_DIR = "../../knx-uf-iconset/raw_svg"
SVG_TEMP_DIR = "svg"
JS_TEMPLATE = "js.template"
JS_DEST_FILE = "../dist/ha-knx-uf-iconset.js"

icons = {}

def getInkscapeVersion() :
    # Calling "inkscape -V" returns a string like "Inkscape 1.0.1 (3bc2e813f5, 2020-09-07)""
    result = subprocess.run([INKSCAPE_EXE, "-V"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return re.match(f"{INKSCAPE_NAME} (\\d+)\\.(\\d+)\\.(\\d+)", result.stdout).groups()

def convertSvg(file) :
    """Convert SVG into Home Assistant compatible format

    Home Assistant can only handle SVG paths. Therefore 

    Step 1: Ungroup all paths
    Step 2: Combine all paths into a single path
    Step 3: Convert strokes to paths
    Step 4: Save file
    """
    actions = "EditSelectAll; " + 10*"SelectionUnGroup; " + "StrokeToPath; SelectionCombine; FileSave"
    result = subprocess.run([INKSCAPE_EXE, "--batch-process", f"--actions={actions}", file], capture_output=True)
    assert result.returncode == 0, ""

def insertIconList(icons):
    result = ""
    for k,v in sorted(icons.items()):
        result += "\t" + f"'{k}': '{v}',\n"
    return result

def main():
    version = getInkscapeVersion()
    assert int(version[0]) >= 1, "Inkscape major version should be >= 1"

    dest_dir = Path(__file__).parent / SVG_TEMP_DIR

    # ensure that destination path exists
    dest_dir.mkdir(parents=True, exist_ok=True)

    # regular expression to find paths in svg
    p = re.compile(r'\bd="([^"]*)"')

    source_dir = Path(__file__).parent / SOURCE_DIR
    for svg_src_filename in Path(source_dir).glob("*.svg"):
        print(f"Processing {svg_src_filename.stem}")
        # get destination svg file
        svg_dest_filename = dest_dir / svg_src_filename.name

        # copy file from source directory to svg temp dir
        copyfile(svg_src_filename, svg_dest_filename)

        # convert svg file using inkscape
        convertSvg(svg_dest_filename)

        # read path from svg
        svg_file = open(svg_dest_filename)
        matches = p.findall(svg_file.read())

        assert len(matches) > 0, f"No path found in file {svg_dest_filename.name}"
        if len(matches) > 1:
            print(f"File {svg_dest_filename.name} contains multiple paths: count={len(matches)}")

        icons[svg_dest_filename.stem] = matches[0]
        svg_file.close()

    # update template javascript file
    js_template_filename = Path(__file__).parent / JS_TEMPLATE
    js_template_file = open(js_template_filename)
    js = js_template_file.read()
    js_template_file.close()
    js = js.replace("PLACEHOLDER_ICONSET_NAME", "kuf")
    js = js.replace("PLACEHOLDER_VIEW_BOX", "50 50 260 260")
    js = js.replace("PLACEHOLDER_ICON_LIST", insertIconList(icons))
    
    # write to destination file
    js_dest_filename = Path(__file__).parent / JS_DEST_FILE
    js_dest_file = open(js_dest_filename, "w")
    js_dest_file.write(js)
    js_dest_file.close()


if __name__ == "__main__":
    main()
