[![Fabman on PyPI](https://img.shields.io/pypi/v/fabman.svg)](https://pypi.python.org/pypi/fabman)
[![License](https://img.shields.io/pypi/l/fabman.svg)](https://pypi.python.org/pypi/fabman)
[![Python Versions](https://img.shields.io/pypi/pyversions/fabman.svg)](https://pypi.python.org/pypi/fabman)
[![Build Status](https://github.com/utexas-engr-tiw/fabman-api/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/utexas-engr-tiw/fabman-api/actions)
[![Coverage](https://codecov.io/gh/utexas-engr-tiw/fabman-api/branch/main/graph/badge.svg?token=AGABZU5YOJ)](https://codecov.io/gh/utexas-engr-tiw/fabman-api)

# Fabman API 

Library for interfacing with te Fabman API. Created for Texas Inventionworks as part of the Cockrell School of Engineering at the University of Texas at Austin.

Official documentation for the Fabman API can be found [here](https://github.com/FabmanHQ/fabman-api). Live interaction and description of all endpoints can further be found [here](https://fabman.io/api/v1/documentation#/). This library is currently targeting version 2.3.1 of the Fabman API.

## Getting Started

To get started, simply install using pip:
```
pip install fabman
```
which will install the latest stable release for your use. Note that this library is in active, heavy development and the API may change with little warning. To use the latest state of this repo, use the following command:
```
pip install git+https://github.com/utexas-engr-tiw/fabman-api
```

To start interacting with the Fabman API, simply provide your API key:

```
from fabman import Fabman

f = Fabman(API_KEY)
```

From there, you can begin interacting with api endpoints as described in the official documentation. Most top-level methods return an object which manages that object. For example, to get a single member and update that member's name,
```
member = f.get_member(12345)
member.update(firstName="Natalie", lastName="Wynn")
```
All parameters except for IDs are taken in as kwargs and should follow the camelCase naming conventions found on the Fabman API

## Contributing

We would love contributions! We are a small development team. To contribute, familiarize yourself with the code, the layout, make your edits and a pull request. We currently need help with

* Writing Mock Tests
* Coverage of API endpoints
* Real life testing of the API
* Documentation