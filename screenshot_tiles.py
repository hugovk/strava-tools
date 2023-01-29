#!/usr/bin/python3
"""
Make a screenshot of the map after new set of tiles have been collected.

Good for creating an animated GIF.

Assumes "tile" is in the title or description of each.

Requires
1. Chromedriver https://sites.google.com/chromium.org/driver/
2. Data in https://veloviewer.com
3. Data in https://www.statshunters.com
4. pip install selenium

Usage

First, manual stuff

1. Go to https://veloviewer.com/activities
2. Generate CSV
3. Download CSV 1

Then one time to log into StatsHunter with Strava in Selenium's own browser:

4. python3 screenshot_tiles.py --setup

May need to do this next time too, when the session expires. Otherwise, normal run:

5. python3 screenshot_tiles.py

This opens StatsHunter with the last ride, so the page is zoomed for the largest extent,
and takes a screenshot. Next it opens the date picker and selects the next newest, and
takes another screenshots. And repeat until done.

6. Can then animate with something like this:
convert -delay 20 screenshots/*.png -loop 0 screenshots/anim.gif
# https://www.imagemagick.org/Usage/anim_basics/
# -delay=time in 1/100th of a second to pause between frames
# -loop=number of times to cycle, 0 = infinite loop

Or for longer delay at end of loop, prefix last screenshot with 'last-':

convert -delay 30 screenshots/202*.png -delay 100 screenshots/last-*.png \
    -loop 0 screenshots/anim.gif
"""
import argparse
import calendar
import csv
import os
import sys
import time
from pprint import pprint  # noqa: F401

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def load_csv(csv_file):
    data = []

    with open(csv_file) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(row)

    print(len(data), "rows found")
    if len(data) == 0:
        sys.exit("No data found")

    return data


def convert_date_string(input_string: str) -> str:
    # 2020-11-15 11:29:44
    # ->
    # 20201115
    new_date = input_string.split()[0].replace("-", "")
    return new_date


def convert_date_string2(input_string: str) -> str:
    # 20201115
    # ->
    # November 2020
    year = input_string[:4]
    month = input_string[4:6]
    month = calendar.month_name[int(month)]
    return f"{month} {year}"


def setup_browser(driver):
    """Do this once and log in to Strava for StatsHunters in Selenium's own Chrome"""
    driver.get("https://www.statshunters.com/heatmap/tiles")
    input("Press 'Enter' after logging in to Strava\n")


def open_page(driver, date):
    url = f"https://www.statshunters.com/heatmap/tiles?to={date}"
    print(url)

    driver.get(url)
    print("wait for main tick to be located...")
    main_spinner = (
        '//div[@class="both"'
        ' and contains(., "Checking for new activities on Strava")'
        ' and contains(., "check_circle")]'
    )
    # TODO Could wait until Activities spinner to turn green,
    # TODO no need to wait for "Checking for new activities on Strava"
    wait = WebDriverWait(driver, 120)
    wait.until(EC.presence_of_element_located((By.XPATH, main_spinner)))
    print("DONE located")

    print("find Close button")
    button = driver.find_element(
        By.XPATH, '//div[@class="ui-button__content"][contains(text(),"Close")]'
    )
    print("click Close button")
    button.click()

    print("wait for main tick to be gone...")
    wait.until(EC.invisibility_of_element_located((By.XPATH, main_spinner)))
    print("DONE is gone")
    time.sleep(1)


def get_date(driver, date):
    filename = f"screenshots/{date}.png"
    if os.path.isfile(filename):
        print(f"File {filename} exists, skipping")
        return
    print(date)

    # span class filter_list
    print("Find/open filter button")
    filter_list = driver.find_element(By.CLASS_NAME, "filter_list")
    filter_list.click()

    # ui-collapsible__header-content
    print("Find/open 'Filter by date'")
    toggles = driver.find_elements(By.CLASS_NAME, "ui-collapsible")
    for toggle in toggles:
        if toggle.text == "Filter by date":
            toggle.click()
            time.sleep(0.1)
            break

    print("Find 'to' date picker")
    datepicker = driver.find_elements(By.CLASS_NAME, "ui-datepicker__content")[1]
    # open it
    datepicker.click()

    # find the right date
    target_month_and_year = convert_date_string2(date)
    target_day = str(int(date[6:8]))  # drop leading zeros

    # calendar popup
    popup = driver.find_elements(By.CLASS_NAME, "ui-datepicker-calendar__body")[1]

    month_and_year = popup.find_element(
        By.CLASS_NAME, "ui-calendar-controls__month-and-year"
    )
    time.sleep(1)

    # Find month
    print(f"Find {target_month_and_year}")
    back_button = popup.find_elements(
        By.CLASS_NAME, "ui-calendar-controls__nav-button"
    )[0]
    while month_and_year.text != target_month_and_year:
        print(month_and_year.text)
        back_button.click()
        time.sleep(1)
    # time.sleep(1)

    # Find day
    print(f"Find {target_day}")
    days = popup.find_elements(By.CLASS_NAME, "ui-calendar-week__date")
    for day in days:
        print(day.text)
        if day.text == target_day:
            day.click()
            break
    time.sleep(1)

    print("Close filter button")
    filter_list.click()
    time.sleep(0.1)

    print(f"save screenshot {filename}")
    driver.save_screenshot(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="TODO",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-c",
        "--csv",
        default="/tmp/Downloads/activities.csv",
        help="VeloViewer (not Strava) CSV filename",
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Set up by manually logging in to Strava, required on first run",
    )
    args = parser.parse_args()

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-data-dir=selenium")
    driver = webdriver.Chrome(options=chrome_options)

    if args.setup:
        setup_browser(driver)

    activities = load_csv(args.csv)

    dates = set()
    for activity in activities:
        if (
            "tile" in activity["Name"].lower()
            or "tile" in activity["Description"].lower()
        ):
            # pprint(activity)
            print(activity["When"], activity["Name"], activity["Description"])
            date = convert_date_string(activity["When"])
            dates.add(date)

    # Convert set to sorted list
    dates = sorted(list(dates), reverse=True)
    # dates.append("20200404")  # TEMP the day before first intentional tile collecting
    pprint(dates)

    open_page(driver, dates[0])

    for date in dates:
        get_date(driver, date)

    # driver.close()
