# Pip integration
- to install from git+pip: `pip install 
  git+https://github.
  com/egslava/sublesee.git#subdirectory=soft`       
- to check locally, run `bash check_local.bash` 
  **INSIDE pip directory**. Currently tested on 
  macOs only.


## Development
To install pip package locally and check its 
content:

1. Go to some directory
2. `deactivate ; rm -rf venv ; python3 -m venv venv 
   && source venv/bin/activate && pip install 
   --no-cache-dir -U $to_install && echo 
   $pkgs/sublesee 
   && ls $pkgs/sublesee && echo $pkgs && ls $pkgs`
3. Check that output contains only `src.sublesee`'s 
   folder content and doesn't have any test-files.
4. The building system generates `src/sublesee.egg` 
   and `soft/build`