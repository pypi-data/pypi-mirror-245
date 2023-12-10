from setuptools import setup, find_packages

setup(
    name='PyConversionKit',
    version='0.0.1',
    author='Mukul Ganwal',
    author_email='mukulgawnal@gmail.com',
    packages=find_packages(),
    description='A comprehensive toolkit for converting various file formats in Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/FanFeast/PyConversionKit.git',
    install_requires=[
        # List your package dependencies here, if any
    ],
    classifiers=[
        # Classifiers help users find your project
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
