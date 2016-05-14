import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'alembic',
    'celery',
    'nltk',
    'oauth2',
    'pycountry',
    'pymysql',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'requests[security]',
    'SQLAlchemy==1.0.8',
    'spotipy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    ]

setup(name='popcrn',
      version='0.0',
      description='popcrn',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Sahil Prasad',
      author_email='sahil_prasad@brown.edu',
      url='https://www.github.com/sahilprasad/popcrn',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='popcrn',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = popcrn:main
      [console_scripts]
      initialize_popcrn_db = popcrn.scripts.initializedb:main
      """,
      )
