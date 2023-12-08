from setuptools import setup, find_packages

setup(
    name='reportzz_ai',
    version='0.1.6',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Reportzz is a Python project that is designed to generate reports.',
    long_description=open('README.md').read(),
    install_requires=[
        'pytest',
        # ... other dependencies ...
    ],
    url='https://github.com/zzirakadze/reportzz',
    author='Zura Zirakadze',
    author_email='zirakadzez@gmail.com',
    include_package_data=True,
    entry_points={
        'pytest11': [
            'name_of_plugin = data_collection.conftest',
        ],
    },
    # ... other configurations ...
)
