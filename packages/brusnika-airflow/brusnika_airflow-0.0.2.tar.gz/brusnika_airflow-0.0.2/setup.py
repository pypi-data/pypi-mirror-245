"""Setup for package"""

from setuptools import find_packages, setup

setup(
    name="brusnika_airflow",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        "pendulum",
        "sqlalchemy",
    ],
)
