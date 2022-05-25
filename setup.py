from setuptools import setup, find_packages

setup(name='opensubtitles-dl',
      version='1.0.0',
      description='opensubtitles-dl',
      packages=['opensubtitles_dl', ],
      install_requires=['click', 'requests', ],
      entry_points={
          'console_scripts': [
              'opensubtitles-dl=opensubtitles_dl.manager:cli',
          ]
      }
)
