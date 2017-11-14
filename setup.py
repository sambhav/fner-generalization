from setuptools import setup, find_packages

setup(
    name='fners',
    version='0.1',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        fners=fner_oversampling.oversampling:cli
    ''',
)
