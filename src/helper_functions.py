import os, re, mimetypes, subprocess

import pysrt

from exceptions import *
from config import *

si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
system = lambda command: subprocess.call(command, startupinfo=si, shell=True)

def replace_ext(filename, ext):
  return '.'.join(filename.split('.')[:-1]) + f'.{ext}'

def has_srt(filename):
  filetype = mimetypes.guess_type(filename)[0]
  if filetype is not None:
    if 'video' not in filetype:
      return False
  else:
    return False
  try:
    system(f'{ffmpeg} -i "{filename}" -c copy -map 0:s -f null - -v 0 -hide_banner && echo 1 >> output.txt || echo 0 >> output.txt')
    has = "1" in open('output.txt', 'r').read()
    os.remove('output.txt')
    return has
  except Exception as e:
    raise VidConvertError("Error converting video")

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext.strip()

def extract_srt(filepath):
  filename = filepath.split('/')[-1]
  output_srt = replace_ext(filename, "srt")
  output_txt = replace_ext(filename, "txt")
  output_srt_path = f'{output_folder_srt}/{output_srt}'
  output_txt_path = f'{output_folder_txt}/{output_txt}'
  try:
    system(f'call {ffmpeg} -i "{filepath}" -map 0:s:0? "{output_srt_path}" -y')
    subs = pysrt.open(output_srt_path)
    lines = []
    for sub in subs:
      lines.append(cleanhtml(sub.text))
    open(f'{output_txt_path}', 'w', encoding='utf8').write('\n'.join([l for l in lines if l]))
  except:
    raise ExtractSrtError(f"Error extracting srt: ({output_srt_path})")