# coding: utf-8

# SICOR is a freely available, platform-independent software designed to process hyperspectral remote sensing data,
# and particularly developed to handle data from the EnMAP sensor.

# This file contains the package setup tools.

# Copyright (C) 2018  Niklas Bohn (GFZ, <nbohn@gfz-potsdam.de>),
# German Research Centre for Geosciences (GFZ, <https://www.gfz-potsdam.de>)

# This software was developed within the context of the EnMAP project supported by the DLR Space Administration with
# funds of the German Federal Ministry of Economic Affairs and Energy (on the basis of a decision by the German
# Bundestag: 50 EE 1529) and contributions from DLR, GFZ and OHB System AG.

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.


from setuptools import setup, find_packages

__author__ = "Niklas Bohn"


with open("README.rst") as readme_file:
    readme = readme_file.read()

version = {}
with open("sicor/version.py", encoding="utf-8") as version_file:
    exec(version_file.read(), version)

req = [
    "arosics>=1.2.4",
    "cachetools",
    "cdsapi",
    "cerberus",
    "dicttoxml",
    "dill",
    "ecmwf-api-client",
    "gdal",
    "gdown",
    "geoarray",
    "glymur",
    "h5py",
    "isofit",
    "iso8601",
    "jsmin",
    "matplotlib",
    "mpld3",
    "netCDF4",
    "numba",
    "numpy",
    "openpyxl",  # implicitly required by pandas.read_excel()
    "pandas",
    "pillow",
    "pint",
    "psutil",
    "py_tools_ds",
    "pygrib",
    "pyprind",
    "pyproj",
    "pyrsr",
    "requests",
    "scikit-image>=0.20.0",
    "scikit-learn",  # might need <=0.24.0 for Landsat/Sentinel-2 cloud classifiers
    "scipy",
    "spectral",
    "sympy",
    "tables",
    "tqdm",
    "xlrd"  # Excel support for pandas
    ]

req_setup = ["setuptools-git"]  # needed for package_data version controlled by GIT

req_test = req + [
    "enpt>=0.17.1",
    "flake8",
    "ipython_memory_usage",
    "mock",
    "pycodestyle",
    "pydocstyle",
    "pylint",
    "pyorbital",  # needed to de-serialize a dill file from GeoMultiSens
    "pytest",
    "pytest-cov",
    "pytest-reporter-hmtl1",
    "sphinx",
    "sphinx-argparse",
    "sphinx_rtd_theme",
    "urlchecker",
]

setup(
    authors="Niklas Bohn, Daniel Scheffler, Maximilian Brell, André Hollstein, René Preusker",
    author_email="nbohn@gfz-potsdam.de",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
    description="Sensor Independent Atmospheric KCorrection",
    data_files=[
        ("data", [
            "sicor/sensors/S2MSI/GranuleInfo/data/S2_tile_data_lite.json",
            "sicor/sensors/S2MSI/data/S2A_SNR_model.xlsx",
            "sicor/AC/data/k_liquid_water_ice.xlsx",
            "sicor/AC/data/newkur_EnMAP.dat",
            "sicor/AC/data/fontenla_EnMAP.dat",
            "sicor/AC/data/conv_fac_fon_lut.dill"
        ])],
    keywords=["SICOR", "EnMAP", "EnMAP-Box", "hyperspectral", "remote sensing", "satellite", "atmospheric correction"],
    include_package_data=True,
    install_requires=req,
    license="GNU General Public License v3 (GPLv3)",
    long_description=readme,
    long_description_content_type="text/x-rst",
    name="sicor",
    package_dir={"sicor": "sicor"},
    package_data={"sicor": ["AC/data/*", "tables/*"]},
    packages=find_packages(exclude=["tests*", "examples"]),
    python_requires='>=3.8',
    scripts=[
        "bin/sicor_ac.py",
        "bin/sicor_ecmwf.py",
        "bin/sicor_ac_EnMAP.py"
    ],
    setup_requires=req_setup,
    test_suite="tests",
    tests_require=req_test,
    url="https://git.gfz-potsdam.de/EnMAP/sicor",
    version=version["__version__"],
    zip_safe=False
)
