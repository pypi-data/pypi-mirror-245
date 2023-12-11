from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='git-assistente',
    version='0.0.1',
    license='MIT License',
    author='CarlosAllberto',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='dasilvacarlosalberto344@gmail.com',
    keywords='git assistente',
    description=u'um assistente do Git para subir projetos no GitHub',
    packages=['git_assistente'],
    install_requires=['colorama', 'dankware'],)