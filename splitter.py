#!/usr/bin/env python3
"""
Chop out a long paused section of a GPX track

For example if paused when on a train

Still saves each file in a single file, but puts each split segment in a new <trkseg>

* Saves a backup of the split files in a split-backup directory
* Split files are saved in a split directory
* Original files aren't changed
"""
import argparse
import copy
import glob
import math as mod_math
import shutil
from multiprocessing import Pool
from pathlib import Path

import gpxpy  # pip3 install gpxpy
import gpxpy.gpx
from gpxpy.geo import ONE_DEGREE
from termcolor import cprint  # pip3 install termcolor
from tqdm import tqdm  # pip3 install tqdm

# from pprint import pprint


def precompute_max(max_distance):
    """Precompute max distance to speed up maths"""
    return (max_distance / ONE_DEGREE) ** 2


def distance_less_than(point1, point2, max2):
    """Check if the distance in metres between point1 and point2 is less than max2
    max2 is (max/ONE_DEGREE)^2

    It's possible to call point1.distance_2d(point2),
    but let's takes some shortcuts

    max2 = precompute_max(args.max)
    ...
    point1.distance_2d(point2) < max2
    # 500000 loops, best of 5: 883 nsec per loop

    point1.distance_2d(point2) < precompute_max(max)
    # 200000 loops, best of 5: 1.06 usec per loop

    point1.distance_2d(point2) < max
    # 200000 loops, best of 5: 1.44 usec per loop
    """
    # print(point1.latitude, point1.longitude)
    latitude_1 = point1.latitude
    latitude_2 = point2.latitude
    longitude_1 = point1.longitude
    longitude_2 = point2.longitude

    coef = mod_math.cos(latitude_1 / 180.0 * mod_math.pi)
    x = latitude_1 - latitude_2
    y = (longitude_1 - longitude_2) * coef

    distance_2d2 = x * x + y * y

    return distance_2d2 < max2


def backup(filename, dry_run):
    """Make a backup of this file in a new subdirectory"""
    subdir = Path("split-backup")
    new_filename = subdir.joinpath(Path(filename))

    if not dry_run:
        new_filename.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(filename, new_filename)


def save_gpx(gpx, filename, dry_run):
    """Save this GPX with the same name in a new subdirectory"""
    subdir = Path("split")
    new_filename = subdir.joinpath(Path(filename))

    if not dry_run:
        new_filename.parent.mkdir(parents=True, exist_ok=True)
        with open(new_filename, "w") as f:
            f.write(gpx.to_xml())

    cprint(new_filename, "green")


def split_gpx(filename, max_distance, max2, dry_run):
    gpx_file = open(filename)
    try:
        gpx = gpxpy.parse(gpx_file)
    except gpxpy.gpx.GPXException as e:
        print(gpx_file)
        cprint(f"Cannot parse {filename}: {e}", "red")
        return

    new_gpx = copy.deepcopy(gpx)
    new_gpx.tracks = []
    edit_made = False

    for track in gpx.tracks:
        new_track = copy.deepcopy(track)
        new_track.segments = []
        # print(track.name, track.type)

        for segment in track.segments:
            new_segment = gpxpy.gpx.GPXTrackSegment()
            last_point = None
            for point in segment.points:
                if not last_point:
                    # Add the first point to the current segment
                    new_segment.points.append(point)
                else:
                    less_than = distance_less_than(point, last_point, max2)
                    if less_than:
                        # d = point.distance_2d(last_point)
                        # if d < max_distance:  # metres

                        # Add the point to the current segment
                        new_segment.points.append(point)
                    else:
                        edit_made = True
                        # Start a new segment
                        new_track.segments.append(new_segment)
                        new_segment = gpxpy.gpx.GPXTrackSegment()
                        new_segment.points.append(point)

                last_point = point

            new_track.segments.append(new_segment)
        new_gpx.tracks.append(new_track)

    if edit_made:
        # print(len(gpx.tracks.segments), filename)
        # gpx.tracks = [new_track]
        backup(filename, dry_run)
        save_gpx(new_gpx, filename, dry_run)


def nonrecursive_find(inspec):
    return glob.glob(inspec)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Chop out long paused sections of GPX tracks, "
        "eg. if paused on a train, and save into split/ subdir",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-i", "--inspec", default="activities/*.gpx", help="Input file spec"
    )
    parser.add_argument(
        "-m",
        "--max",
        metavar="metres",
        default=4000,
        type=int,
        help="Max distance between points",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Read only, don't write any new files",
    )

    args = parser.parse_args()
    print(args)

    filenames = nonrecursive_find(args.inspec)
    print(len(filenames), "found")

    max2 = precompute_max(args.max)

    # Sequential: eg. 7m6s
    # for filename in filenames:
    #     split_gpx(filename, args.max, max2, args.dry_run)

    # Parallel: eg. 3m46s
    pool = Pool()  # Use max available, or specify like processes=4
    pbar = tqdm(total=len(filenames), unit="gpx")

    def update(*a):
        pbar.update()

    results = []
    for filename in filenames:
        results.append(
            pool.apply_async(
                split_gpx,
                args=(filename, args.max, max2, args.dry_run),
                callback=update,
            )
        )
        # pool.apply_async(split_gpx, args=(filename, args.max, max2, args.dry_run))
    pool.close()

    for r in results:
        r.get()

    pool.join()
