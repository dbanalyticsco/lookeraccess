from setuptools import setup, find_packages

setup(
    name='lookeraccess',
    version='0.0.1',
    py_modules=['lookeraccess'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        lookeraccess=lookeraccess.cli:cli
    ''',
)