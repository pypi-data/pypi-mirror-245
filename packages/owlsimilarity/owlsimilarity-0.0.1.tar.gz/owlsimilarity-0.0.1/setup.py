from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='owlsimilarity',
    version='0.0.1',
    license='GNU GENERAL PUBLIC LICENSE',
    author='Edgar Henrique de Oliveira Lira',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='edgar.jj.29@gmail.com',
    keywords=['Relatedness Measure', "Similarity Measure", "Ontology Measure", "Ontology"],
    description=u'Library with implementations of the main similarity and relatedness measures for ontologies.',
    packages=['owlsimilarity'],
    install_requires=['pandas', "owlready2"],)