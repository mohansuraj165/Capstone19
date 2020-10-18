# OSM Mapper
Developed a software tool that converts raw location data from OpenAddresses and OpenStreetMap into a unified XML format that incorporates new access locations into navigation systems. 

## Prerequisites
Python 3.x
Tkinter for GUI
Windows and MAC have Tkinter packaged with python. For Ubuntu install package ‘python3-tkinter’

Jellyfish package
Pip install jellyfish

OSMPythonTools package
Pip install osmpythontools

## Errors and issues
While installing OSMPythonTools library

Error: failed building wheel for json

Steps: 
	
  •	Update setuptools and wheel package. On cmd run “pip install -U setuptools”, “pip install -U wheel”
	
  •	Download apprppriate .whl file from https://www.lfd.uci.edu/~gohlke/pythonlibs/#spacy based on the version of python used (Eg: For 64 bit machine and python3.7 download ujson‑1.35‑cp37‑cp37m‑win_amd64.whl). Copy the file in your python installation (C:\Program Files\Python37) and install “pip install ujson-1.35-cp37-cp37m-win_amd64.whl”. 
