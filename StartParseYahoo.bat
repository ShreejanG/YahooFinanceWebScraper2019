PAUSE
call DeleteJSON.bat
FOR /F "tokens=*" %%i IN (StockTickers.txt) DO python yahoo.py %%i
PAUSE