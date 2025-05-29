from setuptools import setup, find_packages

setup(
    name='funct_utils',
    version='0.1',
    packages=find_packages(),
    install_requires=['numpy'],
    author='Il Tuo Nome',
    author_email='tuo@email.com',
    description='Libreria per calcolo FWHM e rilevamento picchi',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Alberto260699/funct_utils',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
