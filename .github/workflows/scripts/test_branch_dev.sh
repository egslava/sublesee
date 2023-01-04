function on_exit() {
  rm -rf $GENERATED
}
trap "on_exit" EXIT


# smoke tests
BASE=.github/workflows/scripts
DATA=$BASE/data
GENERATED=$DATA/generated
mkdir $GENERATED
sublesee srt2xlsx $DATA/1.Eng.srt $GENERATED/1.xlsx
sublesee xlsx2srt $GENERATED/1.xlsx $GENERATED/1.srt

# can't handle BOM, so I just removed it from
# the test file
diff -bB -C 3 \
  $DATA/1.Eng.srt \
  $GENERATED/1.srt\
  || {
    echo "xlsx2srt failed to restore the original srt"\
          " file. See the diff above";
    exit 1;
  }

sublesee srt2html $DATA/1.Eng.srt $GENERATED/1.html
on_exit

cd soft
pytest
