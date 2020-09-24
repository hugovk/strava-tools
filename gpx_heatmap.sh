#!/bin/bash

# Run on in a folder full of GPX files.
# Creates heatmaps.

# Run like:
# gpx_heatmap.sh input_files output_file_infix

# For example:
# ./gpx_heatmap.sh "activities/kilometrikisa-2019/*.gpx" kilometrikisa-2019

# Requires:
# * heatmap.py

# Create heatmap. Uses http://www.sethoscope.net/heatmap/
WIDTH=1280
# ZOOM=14
OUT_PREFIX=heatmap

OUT_INFIX=$2
INDIR=$1

out_name="$OUT_PREFIX-$OUT_INFIX"

HEATMAPPY="python3 /Users/hugo/github/heatmap/heatmap.py"


# First one saves processed data to a file, for others to load

# OSM map
time $HEATMAPPY --width $WIDTH --decay 0.1 -B 0.8  $INDIR --osm --save /tmp/$out_name.data -o "$out_name-osm.png"

# Black background map
time $HEATMAPPY --width $WIDTH --decay 0.1 --background black --load /tmp/$out_name.data -o "$out_name-black.png"

# Toner map
time $HEATMAPPY --width $WIDTH --decay 0.1 -B 0.8 --osm --osm_base http://b.tile.stamen.com/toner --load /tmp/$out_name.data -o "$out_name-toner.png"

# Watercolor map
time $HEATMAPPY --width $WIDTH --decay 0.1 -B 0.8 --osm --osm_base http://b.tile.stamen.com/watercolor --load /tmp/$out_name.data -o "$out_name-watercolor.png"

# del %OUT_PREFIX%all.png
# normalise -i %OUT_PREFIX%$WIDTH*.png -o %OUT_PREFIX%$WIDTHnormalised -n mode
# contact_sheet -i %OUT_PREFIX%$WIDTHnormalised\* -o %OUT_PREFIX%$WIDTH-all.png %3 %4 %5 %6 %7 %8 %9

contact_sheet.py -i "$out_name-*" -p 20 -m 20 -v -o "$out_name-contact_sheet.png"

open "$out_name-*"

echo "Generated using <a href="http://www.sethoscope.net/heatmap/" rel="nofollow">Seth Golub's heatmap.py</a>"

echo "Map tiles by <a href="http://stamen.com/" rel="nofollow">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0" rel="nofollow">CC BY 3.0</a>. Data [and map tiles] by <a href="http://openstreetmap.org/" rel="nofollow">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0" rel="nofollow">CC BY SA</a>."

echo "Tags:"

echo "map, Stamen, OSM, OpenStreetMap, Watercolor, Toner, Stamen Maps, Stamen Watercolor, Stamen Toner, Experiment, heatmap.py, Stamen Map, kartta, heatmap, GPX heatmap, pixel:tool=contact_sheet, pixel:tool=gpx_heatmap"


# End of file
