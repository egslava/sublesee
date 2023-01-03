python3 -m pip install git+https://"$USER":"$TOKEN"@github.com/"$USER"/sublesee.git@dev#subdirectory=soft

# smoke tests
BASE=.github/workflows/scripts/
DATA=$BASE/data
sublesee srt2xlsx $DATA/1.Eng.srt
sublesee xlsx2srt $DATA/1.Eng.srt.xlsx
diff -ZbB -c \
  $DATA/1.Eng.srt \
  $DATA/1.Eng.srt.xlsx.srt\
  || {
    echo "xlsx2srt failed to restore the original srt"\
          " file. See the diff above";
    exit 1;
  }

sublesee srt2html $DATA/1.Eng.srt
