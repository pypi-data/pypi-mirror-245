from setuptools import setup, find_packages

setup(
    name='mdataset',
    version='0.1.0',
    author='TAWSIF AHMED',
    author_email='sleeping4cat@outlook.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'nougat-ocr',
        'transformers',
        'idisplay',
        'torch',
        'sentencepiece',
        'duckduckgo-search',
        'BASC-py4chan',
        'pytube',
        'tqdm',
        'flask',
        'requests',
        'beautifulsoup4',
        'datasets',
        'petals',
        'kaggle',
        'ydata-synthetic==1.3.0',
        'scap4chan',
        



    ],
)
