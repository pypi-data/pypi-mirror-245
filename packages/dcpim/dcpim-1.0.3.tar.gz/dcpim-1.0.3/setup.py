""" Setup file fopr PyPi. """
from setuptools import setup
import dcpim

setup(
  name = 'dcpim',
  packages = ['dcpim'],
  install_requires = ['boto3'],
  version = dcpim.dcpim.__VERSION__,
  description = 'This is a general purpose Python 3.x library used by DCPIM.',
  author = 'Patrick Lambert',
  license = 'MIT',
  author_email = 'patrick@dendory.ca',
  url = 'https://github.com/dcpim/utils',
  download_url = 'https://github.com/dcpim/utils/archive/master.zip',
  keywords = ['dcpim', 'dynamodb', 'aws', 'util'],
  classifiers = [],
)
