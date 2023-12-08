from setuptools import setup, find_packages

setup(
    name='prac_testing',
    version='0.1',
    packages=find_packages(),
    package_data={'prac_testing': ['data/*']},
    include_package_data=True,
    description='A small package to provide code',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='savioratharv',
    author_email='savioratharv2003@gmail.com',
    url='https://github.com/savioratharv/prac_testing',
    # Add more if needed
)
