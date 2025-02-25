@echo off
echo Importing Crime Index data up to 202412
python main.py -e .txt -type ci -createDatabase -delimiter "," -importSchema "data" -importDatabase "crime_index" -f ./data/crime_index/GroupedDatafiles.csv
echo Finished importing Crime Index