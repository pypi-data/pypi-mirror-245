from setuptools import setup, find_packages

setup(
    name='einvoice',
    version='0.1.0',
    author='Hemanth Sai',
    author_email='mannehemanthsai@gmail.com',
    description='Extract embedded information from einvoice Secure QR Code.',
    packages=find_packages(),
    install_requires=['ultralytics>=8.0.209',
                      'opencv-python', 'pyzbar==0.1.9', 'pdf2image'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
