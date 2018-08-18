from setuptools import setup

setup(
    name='stedr',
    version=0.1,
    py_modules=['stedr'],
    install_requires=[
        'Click',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        stedr=stedr:cli
    '''
)
