python3 -m pip install git+https://"$USER":"$TOKEN"@github.com/"$USER"/sublesee.git@dev#subdirectory=soft

# smoke tests
BASE=.github/workflows/scripts/
DATA=$BASE/data
sublesee srt2xlsx $DATA/1.Eng.srt
sublesee xlsx2srt $DATA/1.Eng.srt.xlsx
cmp --silent\
  $DATA/1.Eng.srt\
  $DATA/1.Eng.srt.xlsx.srt\
  || {
    echo "xlsx2srt failed to restore the original srt file";
    echo "The original file: "
    cat $DATA/1.Eng.srt
    echo "\n\nThe restored file: "
    cat $DATA/1.Eng.srt.xlsx.srt
    echo "Difference: "
    diff $DATA/1.Eng.srt $DATA/1.Eng.srt.xlsx.srt
    exit 1;
  }

sublesee srt2html $DATA/1.Eng.srt
