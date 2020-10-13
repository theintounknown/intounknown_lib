Libraries that I build and use on Twitch

# Install dependencies
pip install -r requirements.txt

# Uninstall all packages
pip freeze | xargs pip uninstall -y

# Run unit tests
nose2 -t core_lib/ -s tests/unit/

