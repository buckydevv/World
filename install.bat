@echo off
set ERRORLEVEL=0

echo [1/5] preparing...
:: check if java and python is installed.
where python
if %ERRORLEVEL% NEQ 0 ( echo error: you don't have python installed. please install python through python.org/downloads. && goto end )
where java
if %ERRORLEVEL% NEQ 0 ( echo error: you don't have java installed. please install java through java.com/download. && goto end )

:: check if requirements.txt and lavalink.jar exists in the current directory
if not exist requirements.txt ( echo error: there is no requirements.txt in the current directory. && goto end )
if not exist lavalink.jar ( echo error: there is no lavalink.jar in the current directory. && goto end )

echo [2/5] installing virtual environment...
python -m pip install virtualenv
python -m venv %cd%\env
call %cd%\env\Scripts\activate.bat

echo [3/5] installing pip requirements...
python -m pip install -r requirements.txt

echo [4/5] opening lavalink.jar file...
java -jar lavalink.jar

echo [5/5] running bot.py file...
python bot.py

:end

:: cOpYRiGHT (c) 2021 nUlL & CoNtribUTors
:: ALl rIGhtS REserVED!
::
::     HTtpS://giTHub.cOm/VIeRoferNaNDo
::
:: PLeaSe no REMOVe coPyrigHT ShUAnA :D 