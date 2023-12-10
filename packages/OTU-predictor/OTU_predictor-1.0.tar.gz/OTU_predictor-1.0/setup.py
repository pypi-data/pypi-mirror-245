# setup.py
from setuptools import setup, find_packages

setup(
    name='OTU_predictor',
    version='1.0',
    packages=find_packages(),
    package_data={'OTU_predictor': ['model/*.joblib']},
    install_requires=[
        'pandas',
        'scikit-learn',
        'joblib',
    ],
)
