@echo off
cd /d "D:\hotel manager"  :: <-- your app folder
echo Starting Flask server...
start http://127.0.0.1:5000
flask run