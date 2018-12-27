#!/usr/bin/python3
"""
The Strava bulk export includes the original files, which may be FIT files.
These are difficult to convert to GPX files.
This script can be used to download the GPX version from Strava.

First you need the Strava cookies so you can use wget:

Log in to Strava with Firefox

Add this add-on to Firefox:
https://addons.mozilla.org/en-GB/firefox/addon/cookies-txt/?src=search

Click the add-on to download cookies.txt

Remove non-Strava cookies:
$ grep strava cookies.txt > strava_cookies.txt && mv strava_cookies.txt cookies.txt

Put your activities.csv and activities/ next to this script and test with:
$ python3 download_fit_as_gpx.py --dry-run

Then:
$ python3 download_fit_as_gpx.py
"""

import argparse
import os
import time

from rename_activities import load_csv, output_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download GPX version of FIT files from Strava",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-c", "--csv", default="activities.csv", help="CSV filename")
    parser.add_argument(
        "-n", "--dry-run", action="store_true", help="Don't download anything"
    )
    args = parser.parse_args()

    activities = load_csv(args.csv)

    for activity in activities:
        # We want to rename the file like 20141207-152233-Ride.gpx
        # print(activity)
        infile = activity["filename"]

        if ".fit" in infile:
            outfile = output_file(activity, ext=".gpx")
            url = "https://www.strava.com/activities/{}/export_gpx".format(
                activity["id"]
            )
            cmd = "wget --no-clobber --load-cookies cookies.txt {} -O {}".format(
                url, outfile
            )
            print(cmd)

            if not args.dry_run:
                os.system(cmd)
                time.sleep(1)
