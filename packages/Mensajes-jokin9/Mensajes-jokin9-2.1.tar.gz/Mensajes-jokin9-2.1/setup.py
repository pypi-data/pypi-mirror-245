from setuptools import setup, find_packages

setup (
    name='Mensajes-jokin9',
    version='2.1',
    description='Un paquete para saludar y despedir',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Joaquin Corbo',
    author_email='joaquin.corbo9@gmail.com',
    url='',
    license_files=['LINCESE'],
    packages=find_packages(), # Esta funcion busca los ficheron init y agrega esos paquetes con esos ficheros (por eso son importantes los ficheros init)
    scripts=[],
    test_suit='tests',
    install_requires=[paquete.strip() for paquete in open("requirements.txt").readlines()], # Esto instalara las dependencias necesarias, poniendo el nombre de cada uno que dependa nuestro paquete
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities'
    ]
) 