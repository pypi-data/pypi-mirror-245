from setuptools import setup, find_packages
from pypandoc import convert_file
with open('./README.md','r',encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='BdRPCpackage',
    version='1.3',
    author='mabin',
    author_email='595470377@qq.com',
    description='Phylogenetic new sample placement software.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Bin-Ma/bd-rpc',
    python_requires= '>=3.6',
    install_requires=['biopython','pandas','numpy','scipy','scikit-learn','rpy2'],

)

