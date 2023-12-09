# GeoML - Computer Vision library for Satellite Images

GeoML runs image processing and machine vision algorithms specifically designed for satellite images. It aims to make your life easier with powerful tools and utilities.


## Present functionality

- Download data from Google Map Tiles API and load into S3
- Generate datasets of preprocessed images with PCA+HOG, SV+HOG, etc.

## Development Setup

To get started with contributing or using the Geoml library, follow these steps to set up your development environment:

Clone the repository to your local machine:
```bash
git clone https://github.com/pgzmnk/geoml.git
cd geoml
```

Install project dependencies in virtual environment using Poetry:
```bash
python3 -m venv .venv
source .venv/bin/activate
poetry install
```

## Getting Started

Once the development environment is set, you can start using the Geoml library in your projects. The library provides various machine vision algorithms tailored for satellite image analysis. Before diving into the specifics, make sure you have a basic understanding of satellite images and their properties.

Environment variables:
```
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export GOOGLE_API_KEY=
export ROBOFLOW_API_KEY=
```

To use GeoML in your Python script, import it as follows:

```python
import geoml
```

Now you can access the various functions and classes provided by the library to analyze satellite images. For example, to apply a machine learning classifier on an image, you can use the following code snippet:

```
wip...
```

## Contributing

If you find a bug, have a feature request, or want to contribute code, please open an issue or PR.

## Publish

```
poetry config pypi-token.pypi pypi-token-...
poetry build
poetry publish
```


## License

The GeoML library is distributed under the MIT License.
