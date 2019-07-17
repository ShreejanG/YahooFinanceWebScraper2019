@echo off
call DeleteJSON.bat
DEL /Q timeParse.txt
@echo Started Parsing 500 Stocks: %date% %time% >> timeParse.txt
FOR /F "tokens=*" %%i IN (StockTickers.txt) DO python yahoo.py %%i
@echo Ended Parsing 500 Stocks: %date% %time% >> timeParse.txt