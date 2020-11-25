from setuptools import setup, find_packages

setup(
    name='stedr',
    version=0.1,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'configparser',
        'pathlib',
        'options'
    ],
    entry_points='''
        [console_scripts]
        stedr=stedr.main:cli
    '''
)
