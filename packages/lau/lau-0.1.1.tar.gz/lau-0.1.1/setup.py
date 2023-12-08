from setuptools import setup, find_packages

setup(
    name='lau',
    version='0.1.1',
    author='Bruce Lau',
    author_email='lqx404@gmail.com',
    packages=find_packages(),
    description='A small example package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/bruc3lau/lau',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)