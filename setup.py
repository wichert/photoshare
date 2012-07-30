import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'zope.sqlalchemy',
    's4u.sqlalchemy',
    'waitress',
    ]

setup(name='photoshare',
      version='0.0',
      description='photoshare',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Wichert Akkerman',
      author_email='wichert@wiggy.net',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      test_suite='photoshare',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = photoshare:main
      [console_scripts]
      initialize_photoshare_db = photoshare.scripts.initializedb:main
      """,
      )

