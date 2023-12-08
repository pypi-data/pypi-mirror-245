# Copyright (C) 2017-2023 Battelle Memorial Institute
# file: setup.py

from setuptools import setup, find_packages, installer

version = open("version", 'r').readline().strip()
long_description = '\n\n'.join(open(f, 'rb').read().decode('utf-8') for f in ['README.rst', 'CHANGELOG.rst'])

setup(
    name='tesp_support',
    version=version,
    author='Trevor Hardy',
    author_email='trevor.hardy@PNNL.gov',
    description='Python support for the Transactive Energy Simulation Platform',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url='https://github.com/pnnl/tesp',
    license='BSD',
    install_requires=[
        'importlib-resources~=6.1.0',
        'h5py~=3.9.0',
        'helics~=3.4.0',
        'pandas~=2.0.3',
        'numpy~=1.24.4',
        'scipy~=1.10.1',
        'matplotlib~=3.7.3',
        'networkx~=3.1',
        'PYPOWER==5.1.16',
        'pyutilib==6.0.0',
        'Pyomo==6.5.0'
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'tesp_support': ['api/datafiles/*.json']
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering'
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'tesp_component = tesp_support.api.data:tesp_component',
            'schedule_server = tesp_support.api.schedule_server:main'
        ]
    }
)
