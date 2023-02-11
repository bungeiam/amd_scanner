@echo off
echo This will install all the needed modules to run the scanner.
pause
python -m pip install --upgrade pip
python -m pip install selenium
python -m pip install webdriver-manager
python -m pip install beautifulsoup4
python -m pip install urllib3
python -m pip install google-api-core
python -m pip install google-api-python-client
python -m pip install google-auth
python -m pip install google-auth-httplib2
python -m pip install google-auth-oauthlib
python -m pip install googleapis-common-protos
python -m pip install html5lib
python -m pip install httplib2
python -m pip install ffmpeg
python -m pip install ffmpy
python -m pip install pydub
python -m pip install SpeechRecognition
python -m pip install oauth2client
python -m pip install lxml
echo All modules installed and ready, press any key to quit. 
pause