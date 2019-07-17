
DEL /Q time.txt

@echo Started: %date% %time% >> time.txt
timeout /T 10
@echo Completed: %date% %time% >> time.txt