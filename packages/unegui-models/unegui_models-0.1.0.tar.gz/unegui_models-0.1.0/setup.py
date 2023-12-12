from setuptools import setup, find_packages

setup(
    name='unegui_models',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    description='A package for shared SQLAlchemy models',
    install_requires=[
        'sqlalchemy',  # List all dependencies required for your models here
        'python-dotenv'
    ],
    python_requires='>=3.6',
    # Add other necessary package metadata
)
