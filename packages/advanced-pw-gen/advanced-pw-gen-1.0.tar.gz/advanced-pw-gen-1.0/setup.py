from setuptools import setup, find_packages
setup(
    name="advanced-pw-gen",
    version="1.0",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={'': ['input_tables/*']},
    requires=[
        ],
    extras_require={
        'dev': [
            'twine',
            'wheel',
            'pytest',
        ]
    },
)