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


