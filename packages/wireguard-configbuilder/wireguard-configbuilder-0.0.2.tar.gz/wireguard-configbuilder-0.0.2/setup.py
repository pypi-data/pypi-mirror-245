from setuptools import find_packages, setup

setup(
  name="wireguard-configbuilder",
  packages=find_packages(),
  entry_points={
      'console_scripts': [
          'wireguard-configbuilder = configbuilder.app:main',
      ]
  },
  scripts=[]
)