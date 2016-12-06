@echo off
REM Call FC and suppress all output if the files match
REM Exit with 1 on difference, 0 on no difference
@fc %1 %2 > fc.out || type fc.out && exit /b 1