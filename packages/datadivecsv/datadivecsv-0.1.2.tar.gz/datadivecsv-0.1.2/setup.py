from setuptools import setup, find_packages

setup(
    name='datadivecsv',
    version='0.1.2',
    packages=find_packages(),
    description='Herramienta de Análisis Exploratorio de Datos para archivos CSV',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Aldo Mellado Opazo',
    author_email='aldomellado.1310@gmail.com',
    url='https://github.com/aldomelladop/datadivecsv.git',
    install_requires=[
        'pandas', 'matplotlib', 'seaborn', 'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
