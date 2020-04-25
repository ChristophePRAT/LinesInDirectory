from setuptools import setup
setup(
    name='Lines In Directory',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'lid=lid:run'
        ]
    }
)