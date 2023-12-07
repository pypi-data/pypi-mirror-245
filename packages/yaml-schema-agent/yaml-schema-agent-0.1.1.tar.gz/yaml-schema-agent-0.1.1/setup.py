from setuptools import setup, find_packages

setup(
    name='yaml-schema-agent',
    version='0.1.1',
    url='https://github.com/nayak-swastik/yaml-schema',
    description='Project to Generate Schema from/to YAML and Also Validate',
    author='Swastik.Nayak',
    author_email='swastik.nayak.eu@gmail.com',
    packages=find_packages(),
    install_requires=['jsonschema'],
    long_description="Currently under development",
    entry_points={
        'console_scripts': ['ysg=YamlSchemaAgent.entry_point:main'],
    }
)
