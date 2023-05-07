from setuptools import setup, find_packages


setup(
    name='ldh',
    version='0.0',
    description='ldh',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='DLCE EVA Dev',
    author_email='dlce.rdm@eva.mpg.de',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'clld>=9.2.2',
        'clldmpg>=4.2',
        'cldfcatalog',
        'clld-glottologfamily-plugin',
        'pyglottolog',
        'sqlalchemy<2',
        'waitress',
        'bs4',
    ],
    extras_require={
        'dev': [
            'flake8',
            'tox',
        ],
        'test': [
            'psycopg2',
            'mock',
            'pytest>=3.6',
            'pytest-clld>=0.4',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
            'selenium',
            'zope.component>=3.11.0',
            'lxml',
        ],
    },
    test_suite="ldh",
    entry_points={
        'console_scripts': [
            'ldh=ldh.__main__:main',
        ],
        'paste.app_factory': [
            'main = ldh:main',
        ],
    })
