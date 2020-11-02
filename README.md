Libraries that I build and use on Twitch
* Wrappers around Tkinter
* State Management Library with Subscribable Events
* Database ORM

# Install dependencies
pip install -r requirements.txt

# Uninstall all packages
pip freeze | xargs pip uninstall -y

# Run unit tests
nose2 -t core_lib/ -s tests/unit/

# To run tkinter on Ubuntu / Debian
sudo apt-get install python3-tk build-essential

# To package library
python setup.py bdist_wheel --universal

# Local Install options
pip3 install .		# local install
pip3 install -e .	# local install and symlinked so svn update will update all project
