from setuptools import setup, find_packages

setup(
    name='k-ktransformer',
    version='0.0.1',
    description='kramers-kronig relation transformer',
    author='choekangrok',
    author_email='chlrkdfhr@gmail.com',
    url='https://github.com/choekangrok/k-k-relation',
    install_requires=[],
    packages=find_packages(exclude=[]),
    keywords=['k-k relation', 'choekangrok','kramers-kronig'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)