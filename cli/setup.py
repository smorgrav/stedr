from setuptools import setup

setup(
    name='stedr',
    version=0.1,
    py_modules=['cli'],
    install_requires=[
        'Click',
        'requests',
        'configparser',
        'pathlib'
    ],
    entry_points='''
        [console_scripts]
        stedr=cli:cli
    '''
)
