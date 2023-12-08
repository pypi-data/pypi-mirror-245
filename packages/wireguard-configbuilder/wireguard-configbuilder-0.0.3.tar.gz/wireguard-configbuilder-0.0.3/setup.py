from setuptools import find_packages, setup

setup(
  name="wireguard-configbuilder",
  packages=find_packages(),
  entry_points={
    'console_scripts': [
      'wireguard-configbuilder = configbuilder.app:main',
      'build = configbuilder.app:build',
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