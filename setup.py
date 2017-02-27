from setuptools import setup, find_packages


setup(
    name='revas',
    version='0.0.1',
    description='Assign Udacity\'s revision automatically!',
    author='Ana Paula Gomes',
    author_email='apgomes88@gmail.com',
    url='https://github.com/anapaulagomes/reviews-assigner',
    packages=find_packages(exclude=('tests'))
)
