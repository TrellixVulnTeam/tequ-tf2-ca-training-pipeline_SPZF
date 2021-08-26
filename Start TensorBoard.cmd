SET OUTPUT_PATH=%cd%\content\output
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --new-window "http://localhost:6006"
tensorboard --logdir %OUTPUT_PATH% 
