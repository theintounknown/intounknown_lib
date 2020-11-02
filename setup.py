from setuptools import setup

setup(
   name='intounknown_lib',
   version='1.0',
   description='IntoUnknown Library from Twitch',
   author='theintounknown',
   author_email='',
   license='MIT',
   packages=['intounknown_lib'],
   include_package_data=True,
   zip_safe=False,
   install_requires=[
      'tornado>6.0<7',
   ]
)