from setuptools import setup

setup(name='jetscrape',
      version='0.1',
      description='Download Jetstar (AU) CC data',
      url='http://github.com/evansgp/jetscrape',
      author='Gareth Evans',
      author_email='evans.g.p@gmail.com',
      packages=['jetscrape'],
      zip_safe=False,
      entry_points={
          'console_scripts': ['jetscrape=jetscrape.command_line:main']
      })
