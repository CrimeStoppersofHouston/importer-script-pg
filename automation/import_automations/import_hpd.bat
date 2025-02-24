@echo off
echo [IMPORT] Importing hpd_202411
python main.py -e .xlsx -type hpd -createDatabase -importSchema "hpd_202411" -importDatabase "hpd" -d ./data/hpd/20241227
echo [IMPORT] Completed hpd_202411 import!
echo [IMPORT] Importing hpd_202412
python main.py -e .xlsx -type hpd -createDatabase -importSchema "hpd_202412" -importDatabase "hpd" -d ./data/hpd/20250131
echo [IMPORT] Completed hpd_202412 import!