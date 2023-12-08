from setuptools import setup, find_packages

setup(
    name='reportzz_ai',
    version='0.1.1',
    packages=find_packages(exclude=['tests*']),
    py_modules=['main', 'conftest'],
    license='MIT',
    description='Reportzz is a Python project that is designed to generate reports.',
    long_description=open('README.md').read(),
    install_requires=['numpy'],
    url='https://github.com/zzirakadze/reportzz',
    author='Zura Zirakadze',
    author_email='zirakadzez@gmail.com'
)