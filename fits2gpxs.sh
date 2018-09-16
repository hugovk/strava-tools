GPSBABELPATH=gpsbabel
# GPSBABELPATH=/Volumes/GPSBabelFE/GPSBabelFE.app/Contents/MacOS/gpsbabel

for FILENAME in activities/*.fit
do
    echo $FILENAME
    $GPSBABELPATH -i garmin_fit -f $FILENAME -o gpx -F $FILENAME.gpx
#    perl fit2gpx $FILENAME > $FILENAME.gpx
done
