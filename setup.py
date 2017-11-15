from setuptools import setup, find_packages

setup(
    name='fnerg',
    version='0.1',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        fnerg=fner_generalization.cli:fnerg
    ''',
)
