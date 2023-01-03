python3 -m pip install git+https://"$USER":"$TOKEN"@github.com/"$USER"/sublesee.git@dev#subdirectory=soft

# smoke tests
sublesee srt2xlsx ./data/1.Eng.srt
sublesee xlsx2srt ./data/1.Eng.srt.xlsx
cmp --silent\
  1.Eng.srt\
  1.Eng.srt.xlsx.srt\
  || { echo "xlsx2srt failed to restore the "\
            "original srt file"; exit 1; }

sublesee srt2html ./data/1.Eng.srt
