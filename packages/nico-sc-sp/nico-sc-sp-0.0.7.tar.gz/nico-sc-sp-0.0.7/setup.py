from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.7'
DESCRIPTION = 'Find covariation patterns between interacted cell types from spatial data.'
LONG_DESCRIPTION = 'A package that performs cell type annotations on spatial transcriptomics data, find the niche interactions and covariation patterns between interacted cell types'

# Setting up
setup(name="nico-sc-sp", #"nico-sc-sp"
    version=VERSION,
    author="Ankit Agrawal",
    author_email="<ankitplusplus@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['scanpy==1.9.6','seaborn==0.12.2','scipy==1.11.3', 'matplotlib==3.7.3','numpy==1.26.1','gseapy==1.0.6', 'xlsxwriter==3.1.9',  'pydot==1.4.2', 'KDEpy==1.1.8', 'leidenalg'],
    keywords=['python', 'niche','spatial transcriptomics','single-cell RNA sequencing','scRNAseq','scRNA-seq','MERFISH','seqFISH','STARmap','nico'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
