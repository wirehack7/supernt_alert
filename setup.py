from distutils.core import setup
import py2exe

setup(console=[{'script': 'main.py'}, ],
      options={"py2exe": {
          "packages": ['urllib', 'bs4'], }}
      )
