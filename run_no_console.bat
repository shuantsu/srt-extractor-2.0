set PYTHONDONTWRITEBYTECODE=1
call env/Scripts/activate
python compile_ui.py
cd src
start pythonw srt_extractor.py