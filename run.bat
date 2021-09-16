@echo off

for /f "delims=" %%x in (settings) do (set "%%x")

for /F "tokens=2" %%i in ('date /t') do set mydate=%%i
set mydate=%mydate:/=-%
set mytime=%time::=-%
set folder=%mydate%_%mytime%

IF "%OUT_DIR%"=="" set OUT_DIR="%folder:~0,-3%_%MARKUP_SYMBOL%_%VISION_MODEL%"

echo "OUT_DIR: %OUT_DIR%"
echo "CHARACTER_LIST: %CHARACTER_LIST%"
echo "MARKUP_SYMBOL: %MARKUP_SYMBOL%"
echo "VISION_MODEL: %VISION_MODEL%"
echo "TESSERACT_MODEL: %TESSERACT_MODEL%"
echo "MINIMUM_CONFIDENCE: %MINIMUM_CONFIDENCE%"

md artifacts\%OUT_DIR%
docker run --rm --name dev-pipeline --mount type=bind,source="%cd%/short_run",target=/pipeline/pdfs --mount type=bind,source="%cd%/artifacts/%OUT_DIR%",target=/pipeline/artifacts -e CHARACTER_LIST=%CHARACTER_LIST% -e MARKUP_SYMBOL=%MARKUP_SYMBOL% -e VISION_MODEL=%VISION_MODEL% -e TESSERACT_MODEL=%TESSERACT_MODEL% -e MINIMUM_CONFIDENCE=%MINIMUM_CONFIDENCE% handaber/pdf-marker:dev

set OUT_DIR=