# strava-tools

[![GitHub Actions status](https://github.com/hugovk/strava-tools/workflows/Lint/badge.svg)](https://github.com/hugovk/strava-tools/actions)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=FFE873)](https://www.python.org/downloads/)
[![Code style: Black](https://img.shields.io/badge/code%20style-Black-000000.svg)](https://github.com/psf/black)

Command-line scripts to do things with Strava.

## Exported data

You can [export an archive of your account](https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export#Bulk)
including your activities in their
original file format (eg. GPX or FIT format, some gzipped, some not) and
named like `971607640.gpx`, `83514080.gpx.gz` and `1243401459.fit.gz`.
(The [Strava support page](https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export#Bulk)
talks of deleting accounts when exporting, but you don't need to delete
anything!)

Here are some tools and notes to have them in a similar format.

First request an archive from your account following [this guide](https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export#Bulk)
and wait for the email. Unzip export_xxxxxxx.zip and move the
`activities` directory and `activities.csv` to the current dir.

### Rename and unzip files

```bash
# Rename files from 1836025202.gpx to 20180912-064451-Ride.gpx
# First a test run without changing files
python3 rename_activities.py --dry-run

# Then do it
python3 rename_activities.py

# Unzip files, deletes GZ files
gunzip activities/*.gz
```

### Convert FIT files

Here's some different methods to convert from FIT to GPX.

#### GPSBabel

If you have any FIT files, you can use [GPSBabel](https://www.gpsbabel.org/)
to convert them:

```bash
# Install on Mac
brew install gpsbabel

# Convert activities/*.fit to activities/*.gpx, keeps FIT files
bash fits2gpxs.sh

# Optionally delete the FIT files
# rm activities/*.fit
```

The Wahoo Elemnt Bolt creates files in FIT version 2. Use GPSBabel 1.6.0 or later, or you may get `fit: Unsupported protocol version 2.0` with older versions such as GPSBabel 1.5.4.

#### FIT-to-GPX

Alternatively, try [Jeffrey Friedl's FIT-to-GPX](http://regex.info/blog/2017-05-13/2799).

1. Download the Java `FitCSVTool` included with the
[free FIT SDK](https://www.thisisant.com/resources/fit/)
([direct download link](https://www.thisisant.com/developer/resources/downloads/)).

```bash
wget https://raw.githubusercontent.com/jeffrey-friedl/FIT-to-GPX/master/fit2gpx
edit fit2gpx fits2gpx.sh
```

Update `JAVA_FITCSV_CMD` in `fit2gpx` to point to the file in the downloaded
SDK and edit `fits2gpxs` to use `fit2gpx` instead of `gpsbabel`.

```bash
# Convert activities/*.fit to activities/*.gpx, keeps FIT files
bash fits2gpxs.sh
```

#### Export as GPX from Strava

Follow the
[Strava guide](https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export#GPX)
to export each file.

Alternatively, use `download_fit_as_gpx.py` to get several. See instructions at
the top of the file.

### Split 'em

Left the GPS recorder paused when on a train? Chop out long paused sections of GPX
tracks, and put them into a split/ subdir.

```bash
pip install --upgrade gpxpy termcolor tqdm
python splitter.py
cp split/activities/*.gpx activities
# backup are at split-backup/activities
```

## Make stuff

### dérive

Generate heatmaps by dragging and dropping files into https://erik.github.io/derive/

### marcusvolz/strava

You can make some great visualisations with
[marcusvolz/strava](https://github.com/marcusvolz/strava). See that repo and
`stravaviz.R` for examples.

* https://twitter.com/hugovk/status/945040232117952512
* https://twitter.com/hugovk/status/947350084429254656
* https://twitter.com/hugovk/status/1043926402616238080

#### Troubleshooting

If you get an error with the [marcusvolz/strava](https://github.com/marcusvolz/strava)
visualisation tools when plotting elevations:

```R
> p3 <- plot_elevations(data)
> ggsave("plots/elevations-all.png", p3, width = 20, height = 20, units = "cm")
Error in FUN(X[[i]], ...) : object 'ele' not found
```

It means not all the coordinate trackpoints in your GPX files have elevation values.

Some options:

* Export those tracks from Strava. Strava makes altitude corrections, which is why their
exports have points with elevation values when original files do not.

* Skip plotting elevations.

### heatmap.py

Generate heatmaps using `gpx_heatmap.py`. See instructions at the top of the file and
update the `HEATMAPPY` path for the file downloaded from https://sethoscope.net/heatmap/
