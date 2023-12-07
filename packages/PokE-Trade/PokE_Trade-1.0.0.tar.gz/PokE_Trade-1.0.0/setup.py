from setuptools import setup, find_packages

setup(
    name='PokE_Trade',
    version='1.0.0',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    description='A package for interacting with the pokemmohub.com API',
    include_package_data=True,
    package_data={"PokE_Trade": ["*.ico", "*.png", "*.csv"]},
    install_requires=[
        'setuptools>=68.0.0',
        'requests>=2.31.0',
        'pandas>=1.2.3',
        'customtkinter>=5.1.3',
        'Pillow>=9.4.0',
        'tkcalendar>=1.6.1'     
    ],
)
