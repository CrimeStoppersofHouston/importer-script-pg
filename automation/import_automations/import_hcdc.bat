@echo off
echo [IMPORT] Importing hcdc_202307
python main.py -e .txt -type hcdc -encoding ANSI -delimiter "\t" -createDatabase -importSchema "hcdc_202307" -importDatabase "hcdc" -d ./data/hcdc/chunks-202309
echo [IMPORT] Completed hcdc_202307 import!
echo [IMPORT] Importing hcdc_202309
python main.py -e .txt -type hcdc -encoding ANSI -delimiter "\t" -createDatabase -importSchema "hcdc_202309" -importDatabase "hcdc" -d ./data/hcdc/chunks-20231111
echo [IMPORT] Completed hcdc_202309 import!
echo [IMPORT] Importing HCDC_202311
python main.py -e .txt -type hcdc -encoding ANSI -delimiter "\t" -createDatabase -importSchema "hcdc_202311" -importDatabase "hcdc" -d ./data/hcdc/chunks-20240106
echo [IMPORT] Completed hcdc_202311 import!
echo [IMPORT] Importing hcdc_202401
python main.py -e .txt -type hcdc -encoding ANSI -delimiter "\t" -createDatabase -importSchema "hcdc_202401" -importDatabase "hcdc" -d ./data/hcdc/chunks-20240316
echo [IMPORT] Completed hcdc_202401 import!
echo [IMPORT] Importing hcdc_202402
python main.py -e .txt -type hcdc -encoding ANSI -delimiter "\t" -createDatabase -importSchema "hcdc_202402" -importDatabase "hcdc" -d ./data/hcdc/chunks-20240330
echo [IMPORT] Completed hcdc_202402 import!
echo [IMPORT] Importing hcdc_202403
python main.py -e .txt -type hcdc -encoding ANSI -delimiter "\t" -createDatabase -importSchema "hcdc_202403" -importDatabase "hcdc" -d ./data/hcdc/chunks-20240427
echo [IMPORT] Completed hcdc_202403 import!
echo [IMPORT] Importing hcdc_202405
python main.py -e .txt -type hcdc -encoding ANSI -delimiter "\t" -createDatabase -importSchema "hcdc_202405" -importDatabase "hcdc" -d ./data/hcdc/chunks-20240629
echo [IMPORT] Completed hcdc_202405 import!
echo [IMPORT] Importing hcdc_202406
python main.py -e .txt -type hcdc -encoding ANSI -delimiter "\t" -createDatabase -importSchema "hcdc_202406" -importDatabase "hcdc" -d ./data/hcdc/chunks-20240727
echo [IMPORT] Completed hcdc_202406 import!
echo [IMPORT] Importing hcdc_202407
python main.py -e .txt -type hcdc -encoding ANSI -delimiter "\t" -createDatabase -importSchema "hcdc_202407" -importDatabase "hcdc" -d ./data/hcdc/chunks-20240831
echo [IMPORT] Completed hcdc_202407 import!
echo [IMPORT] Importing hcdc_202408
python main.py -e .txt -type hcdc -encoding ANSI -delimiter "\t" -createDatabase -importSchema "hcdc_202408" -importDatabase "hcdc" -d ./data/hcdc/chunks-20240928
echo [IMPORT] Completed hcdc_202408 import!
echo [IMPORT] Importing hcdc_202409
python main.py -e .txt -type hcdc -encoding ANSI -delimiter "\t" -createDatabase -importSchema "hcdc_202409" -importDatabase "hcdc" -d ./data/hcdc/chunks-20241026
echo [IMPORT] Completed hcdc_202409 import!
echo [IMPORT] Importing hcdc_202410
python main.py -e .txt -type hcdc -encoding ANSI -delimiter "\t" -createDatabase -importSchema "hcdc_202410" -importDatabase "hcdc" -d ./data/hcdc/chunks-20241123
echo [IMPORT] Completed hcdc_202410 import!
echo [IMPORT] Importing hcdc_202411
python main.py -e .txt -type hcdc -encoding ANSI -delimiter "\t" -createDatabase -importSchema "hcdc_202411" -importDatabase "hcdc" -d ./data/hcdc/chunks-20250104
echo [IMPORT] Completed hcdc_202411 import!
echo [IMPORT] Importing hcdc_202412
python main.py -e .txt -type hcdc -encoding ANSI -delimiter "\t" -createDatabase -importSchema "hcdc_202412" -importDatabase "hcdc" -d ./data/hcdc/chunks-20250125
echo [IMPORT] Completed hcdc_202412 import!