# strava-tools

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

The Wahoo Elemnt Bolt creates files in FIT version 2. Here's some ways to
convert to GPX. However, only GPX exported from Strava worked for me with the
[marcusvolz/strava](https://github.com/marcusvolz/strava) visualistation tools.

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
