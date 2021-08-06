from setuptools import setup

setup(name='opensubtitles-dl',
      version='1.0',
      description='opensubtitles-dl',
      entry_points={
          'console_scripts': [
              'opensubtitles-dl=opensubtitles_dl.manager:cli',
          ]
      }
)
