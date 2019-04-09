from setuptools import setup, find_packages

setup(
    name='lookeraccess',
    version='0.0.1',
    py_modules=['lookeraccess'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests==2.21.0',
        'pyyaml==5.1',
        'pytest==4.4.0',
        'coverage==4.5.3',
        'schema==0.7.0',
        'setuptools==41.0.0'
    ],
    entry_points='''
        [console_scripts]
        lookeraccess=lookeraccess.cli:cli
    ''',
)