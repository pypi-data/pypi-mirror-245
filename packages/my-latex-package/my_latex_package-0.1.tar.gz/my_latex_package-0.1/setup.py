from setuptools import setup, find_packages

setup(
    name='my_latex_package',
    version='0.1',
    packages=find_packages(),
    description='A small LaTeX table generation package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Leo K',
    author_email='essacult@gmail.com',
    url='https://github.com/anxieuse/my_latex_package',
    install_requires=[
    ],
)
