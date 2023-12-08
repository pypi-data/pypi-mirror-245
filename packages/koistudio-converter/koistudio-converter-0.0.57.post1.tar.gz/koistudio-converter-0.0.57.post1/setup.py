import setuptools
import label_studio_converter
import os

# Readme
readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_file, 'r') as f:
    long_description = f.read()

# Module dependencies
requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
with open(requirements_file, 'r') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='koistudio-converter',
    version=label_studio_converter.__version__,
    author='KoiReader Technologies',
    author_email='support@koireader.com',
    description='Format converter add-on for KoiStudio',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/koireader/internal/label-studio-converter',
    packages=setuptools.find_packages(),
    include_package_data=True,
    license='Apache License 2.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    install_requires=requirements,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'label-studio-converter=label_studio_converter.main:main',
        ],
    },
)
