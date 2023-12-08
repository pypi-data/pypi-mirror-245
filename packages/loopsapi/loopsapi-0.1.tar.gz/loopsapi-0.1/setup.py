from setuptools import setup

from loopsapi.__version__ import __version__

with open('README.md', 'r',) as f:
    readme = f.read()

setup(
    name='loopsapi',
    version=__version__,
    install_requires=['requests'],
    packages=['loopsapi'],
    url='https://github.com/abrihter/loopsapi',
    long_description_content_type="text/markdown",
    long_description=readme,
    license='MIT',
    author='abrihter',
    author_email='',
    description='Python wrapper for the Loops.so API',
    keywords=['LOOPS', 'LOOPS.SO', 'API', 'WRAPPER'],
    download_url='https://github.com/abrihter/loopsapi/archive/refs/tags/v0.1.tar.gz',  # noqa E501
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
