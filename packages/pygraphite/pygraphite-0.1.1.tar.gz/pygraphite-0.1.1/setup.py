from setuptools import setup, find_packages

setup(
    name='pygraphite',
    version='0.1.1',
    packages=find_packages(),
    description='A custom Python package for snark graph operations',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='TT',
    author_email='tommyet@btinternet.com',
    url='https://github.com/AlexCheema/Graphite',
    install_requires=[
        'networkx', 'pickle'
    ],
    python_requires='>=3.6',
)
