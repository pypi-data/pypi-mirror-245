from setuptools import setup, find_packages

setup(
    name='myMilePackage1234',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A test python package',
	url='https://github.com/khalad-hasan/myMileConverter',
    author='MK Hasan',
    author_email='khalad.hasan@gmail.com'
)