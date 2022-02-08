SET PYTHONDONTWRITEBYTECODE=1
call env/Scripts/activate
python compile_ui.py
cd src
python srt_extractor.py
pause