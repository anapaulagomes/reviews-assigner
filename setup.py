from setuptools import setup, find_packages


setup(
    name='hunter',
    version='0.0.1',
    description='Hunt some Udacity\'s revision automatically',
    author='Ana Paula Gomes',
    author_email='apgomes88@gmail.com',
    url='https://github.com/anapaulagomes/review-hunter',
    packages=find_packages(exclude=('tests'))
)
