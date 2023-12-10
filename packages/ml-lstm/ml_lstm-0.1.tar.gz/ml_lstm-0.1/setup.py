from setuptools import setup, find_packages

setup(
    name='ml_lstm',
    version='0.1',
    packages=find_packages(),
    package_data={'ml_lstm': ['data/*']},
    include_package_data=True,
    description='Code for LSTM on IMDb Dataset',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='davinci003',
    author_email='freegpt00@gmail.com',
    url='https://github.com/savioratharv/prac_testing',
    # Add more if needed
)