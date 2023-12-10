from setuptools import setup, find_packages
with open("Readme.md", "r") as fh:
    long_description = fh.read()
setup(
    name='einvoice',
    version='0.0.1',
    author='Hemanth Sai',
    author_email='mannehemanthsai@gmail.com',
    description='Extract embedded information from einvoice Secure QR Code.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['einvoice'],
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
