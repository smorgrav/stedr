from setuptools import setup, find_packages

setup(
    name='stedr',
    version=0.1,
    packages=find_packages(),
    install_requires=[
        'Click',
        'requests',
        'configparser',
        'pathlib',
        'options'
    ],
    entry_points='''
        [console_scripts]
        stedr=stedr:cli.cli
    '''
)
