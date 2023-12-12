from setuptools import setup, find_packages
setup(
    name="advanced-pw-gen",
    version="1.1.6",
    packages=find_packages('src'),
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
    author="Arthur Edmiston",
    author_email="arthur.edmiston@soledify.com",
    description="An advanced password generator",
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url="https://gitlab.com/darksidevt/pw_gen",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    maintainer="Arthur Edmiston",
    maintainer_email="arthur.edmiston@soledify.com"
)