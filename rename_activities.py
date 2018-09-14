#!/usr/bin/python3


import argparse
import csv
import os
import pathlib  # Python 3.4+
import sys


def load_csv(csv_file):
    data = []

    with open(csv_file, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(row)

    print(len(data), "rows found")
    if len(data) == 0:
        sys.exit("No data found")

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="TODO", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-c", "--csv", default="activities.csv", help="CSV filename")
    parser.add_argument(
        "-n", "--dry-run", action="store_true", help="Don't rename files"
    )
    args = parser.parse_args()

    activities = load_csv(args.csv)

    for activity in activities:
        # We want to rename the file like 20141207-152233-Ride.gpx
        # print(activity)
        infile = activity["filename"]

        # 2010-05-22 19:39:29
        # ->
        # 20100522-193929
        new_date = activity["date"]
        new_date = new_date.replace("-", "")
        new_date = new_date.replace(":", "")
        new_date = new_date.replace(" ", "-")

        path = pathlib.Path(infile)
        exts = "".join(path.suffixes)
        outfile = "{}-{}{}".format(new_date, activity["type"], exts)
        outfile = path.parent / outfile

        print("{}\t->\t{}".format(infile, outfile))
        if not args.dry_run:
            os.rename(activity["filename"], outfile)
