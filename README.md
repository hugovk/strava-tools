# strava-tools

[![Build Status](https://travis-ci.org/hugovk/strava-tools.svg?branch=master)](https://travis-ci.org/hugovk/strava-tools)
[![Python: 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Command-line scripts to do things with Strava.

## Exported data

Pre-GPDR, you could [bulk export all your activities as GPX files](https://web.archive.org/web/20170322015958/https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export#Bulk)
which were named like `20170921-074112-Ride.gpx`.

Post-GDPR, you can [export an archive of your account](https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export#Bulk)
which includes much more data, however your activities are now in their
original file format (eg. GPX or FIT format, some gzipped, some not) and
named like `971607640.gpx`, `83514080.gpx.gz` and `1243401459.fit.gz`.

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

### Convert FIT v2 files

The Wahoo Elemnt Bolt creates files in FIT version 2. Here's some ways to convert to
GPX.

#### GPSBabel

You can use [GPSBabel](https://www.gpsbabel.org/) to convert them:

```bash
# Install on Mac
brew install gpsbabel

# Convert activities/*.fit to activities/*.gpx, keeps FIT files
bash fits2gpxs.sh
```

If you have something like a Wahoo Elemnt Bolt and get `fit: Unsupported
protocol version 2.0` with GPSBabel 1.5.4, support for FIT v2 was added in
https://github.com/gpsbabel/gpsbabel/pull/163 which hasn't yet been released
(as of 2018-09-14).

Instead, download and open latest build DMG file from
https://github.com/gpsbabel/gpsbabel/releases (was d2c667f for me). Then edit
`fits2gpxs.sh` and update `GPSBABELPATH` to point to the new `gpsbabel` binary,
something like
`GPSBABELPATH=/Volumes/GPSBabelFE/GPSBabelFE.app/Contents/MacOS/gpsbabel` and
run again.

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

## marcusvolz/strava

You can make some great visualisations with
[marcusvolz/strava](https://github.com/marcusvolz/strava). See that repo and
`stravaviz.R` for examples.

### Troubleshooting

If you get an error with the [marcusvolz/strava](https://github.com/marcusvolz/strava)
visualisation tools like:

```R
> data <- process_data("activities")
Error in data.frame(lat = lat, lon = lon, ele = ele, time = time, type = type) :
  arguments imply differing number of rows: 1366, 0, 1
Calls: process_data ... <Anonymous> -> map -> .f -> %>% -> eval -> eval -> data.frame
Execution halted
```

It means not all the coordinate trackpoints in your GPX files have elevation values.
Some options:

* Export those tracks from Strava. Strava makes altitude corrections, which is why their
exports have points with elevation values when original files do not.

* If you don't want elevation profiles (`p3 <- plot_elevations(data)`), edit
  `strava/R/process_data.R` and remove `ele = ele` from
[this line](https://github.com/marcusvolz/strava/blob/b98010aa9ef3ad7e911e7cf26157a2a90e9e8137/R/process_data.R#L32):

```R
result <- data.frame(lat = lat, lon = lon, ele = ele, time = time, type = type) %>%
```

This branch has removed it:
```R
devtools::install_github("hugovk/strava", ref="no-ele")
```

* Use an old version of `marcusvolz/strava`:
```R
devtools::install_github("marcusvolz/strava", ref="4b15bef416955415759361ac10e227ca07c3fde6")
```
