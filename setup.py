from setuptools import setup, find_packages

setup(name='opensubtitles-dl',
      packages=['opensubtitles_dl', ],
      version='1.0.0',
      description='A simple cli tool to download from opensubtitles.org',
      author='Quantum Snowball',
      author_email='quantum.snowball@gmail.com',
      url='https://github.com/quantumsnowball/opensubtitles-dl',
      keywords=['subtitles', 'opensubtitles', ],
      python_requires='>=3.6',
      install_requires=['click', 'requests', ],
      entry_points={
          'console_scripts': [
              'opensubtitles-dl=opensubtitles_dl.manager:cli',
          ]
      }
)
