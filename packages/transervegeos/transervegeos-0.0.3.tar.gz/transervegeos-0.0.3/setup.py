from setuptools import setup, find_packages

setup(
    name='transervegeos',
    version='0.0.3',
    author='Narayan Das Ahirwar',
    author_email='ndahirwar93@gmail.com',
    description='A small example package',
    long_description='file: README.md',
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.8',
    install_requires=[
        'geopandas',
        'shapely',
        # Add other dependencies if needed
    ],
)
