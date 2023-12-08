from setuptools import setup, find_packages

setup(
    name='yaml-schema-agent',
    version='0.2.0-alpha',
    url='https://github.com/nayak-swastik/yaml-schema-agent',
    description='Project to Generate Schema from/to YAML and Also Validate',
    author='Swastik.Nayak',
    author_email='swastik.nayak.eu@gmail.com',
    packages=find_packages(),
    install_requires=['jsonschema'],
    long_description="Alpha version - Internal release.",
    entry_points={
        'console_scripts': ['ysg=YamlSchemaAgent.entry_point:main'],
    }
)
