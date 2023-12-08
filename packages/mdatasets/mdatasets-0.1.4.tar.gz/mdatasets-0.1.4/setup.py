from setuptools import setup, find_packages

setup(
    name='mdatasets',
    version='0.1.4',
    author='TAWSIF AHMED',
    author_email='sleeping4cat@outlook.com',
    description='An one-stop Python library for dataset compilation and processing.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sleepingcat4/Mdataset',
    license='Apache 2.0',
    keywords='dataset compilation processing python library',
    project_urls={
        'Source': 'https://github.com/sleepingcat4/Mdataset',
    },
    packages=find_packages(),
    install_requires=[
        'nougat-ocr',
        'idisplay',
        'sentencepiece',
        'duckduckgo-search',
        'BASC-py4chan',
        'pytube',
        'tqdm',
        'flask',
        'datasets',
        'petals',
        'kaggle',
        'autoscraper',
        'ydata-synthetic==1.3.0',
        'scap4chan',
    ],
)

