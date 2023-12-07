from setuptools import setup, find_packages

setup(
    name='geojson_read',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'shapely',
        'geopandas',
    ],
    entry_points={
        'console_scripts': [
            'geojson_read = geojson_read:main',  # Change 'main' to the actual function name to be called
        ],
    },
)
