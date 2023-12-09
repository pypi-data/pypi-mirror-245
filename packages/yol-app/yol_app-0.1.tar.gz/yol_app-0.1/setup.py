from setuptools import setup, find_packages

setup(
    name='yol_app',
    version='0.1', # Semantic versioning, MAJOR.MINOR.PATCH
    packages=find_packages(exclude=('tests*', 'node_modules*', 'dist*', 'build*', 'yol_app.egg-info*')),
    #packages=find_packages(),
    include_package_data=True,  # This is important to include non-python files
    install_requires=[
        'fastapi',
        'uvicorn',
    ],
    license='Apache License 2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License'
    ],
)
