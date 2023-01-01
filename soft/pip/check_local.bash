soft_path=..
package_name='pymedm'
src_path=$soft_path/src


# 1. to understand the script -- scroll to the bottom
# 2. activate when debugging
#set -o xtrace
# 3. Good luck!

function on_exit() {
  echo 'on_exit'
  cd ..
  rm -rf $tmp
  rm -rf $soft_path/build || echo "No build folder"
  rm -rf $src_path/$package_name.egg-info || echo "No egg-info"
}
trap "on_exit" EXIT


function venv() {
  deactivate  # may not work
  rm -rf venv
  python3 -m venv venv
  python --version
  python3 -m pip --version
  source venv/bin/activate
  pip install --upgrade pip
}


tmp=tmp
mkdir -p $tmp ; cd $tmp
echo `pwd`

_pkgs=venv/lib/python3.9/site-packages

venv
echo `pwd`
pip install --no-cache-dir -U ../$soft_path[test]
#echo $_pkgs/$package_name
#ls $_pkgs/$package_name
#echo $_pkgs
#ls $_pkgs

