import os
from setuptools import find_packages, setup

def get_version():
  with open(os.path.join('configbuilder', '__init__.py')) as f:
    content = f.readlines()

  for line in content:
    if line.startswith('__version__ ='):
      # dirty, remove trailing and leading chars
      return line.split(' = ')[1][1:-2]
  raise ValueError("No version identifier found")

setup(
  name="wireguard-configbuilder",
  packages=find_packages(),
  version = get_version(),
  entry_points={
    'console_scripts': [
      'wireguard-configbuilder = configbuilder.app:main',
      'buildwg = configbuilder.app:build',
    ]
  },
  python_requires=">=3.8",
  # license="License :: OSI Approved :: MIT License",
  classifiers=[
    "Programming Language :: Python",
    # "Programming Language :: Python :: 3",
    # "Operating System :: OS Independent",
    # "Private :: Do Not Upload"
  ],
  scripts=[]
)