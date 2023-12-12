from setuptools import setup, find_packages

setup(
    name='unegui_models',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    description='A library for shared SQLAlchemy models',
    install_requires=[
        'sqlalchemy', 
        'python-dotenv'
        # Add other dependencies required by your models here
    ],
    python_requires='>=3.6',
    # Add other necessary package metadata
)
