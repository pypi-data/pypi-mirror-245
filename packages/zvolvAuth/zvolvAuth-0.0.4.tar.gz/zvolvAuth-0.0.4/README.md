<!-- <p align="center">
  <img src="https://github.com/box/sdks/blob/master/images/box-dev-logo.png" alt= “box-dev-logo” width="30%" height="50%">
</p> -->

# zvolv Python SDK

[![image](http://opensource.box.com/badges/active.svg)]
[![image](https://img.shields.io/pypi/v/boxsdk.svg)]
[![image](https://img.shields.io/pypi/dm/boxsdk.svg)]
[![image](https://coveralls.io/repos/github/box/box-python-sdk/badge.svg?branch=main)]


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Installing](#installing)
- [Getting Started](#getting-started)
- [Versions](#versions)
  - [Supported Version](#supported-version)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Installing

``` console
pip install ZvolvArithmetic 
```

The current version of the SDK is 0.1.0. --- With this release support for
Python 3.8 and earlier (including 2.x). if you're
looking for the code or documentation for v0.1.0

# Getting Started

To get started with the SDK, get a Developer Token from the
Configuration page of your app.

The SDK provides an interactive `arithmetic   ` that makes it easy
to test out the SDK in a REPL. This client will automatically prompt for
a new Developer.

``` pycon
>>> from ZvolvArithmetic import arithmetic_opertion
>>> result = arithmetic_opertion.add_numbers(10,20)
>>> print(result)
>>> 20
>>> result = arithmetic_opertion.sub_numbers(10,20)
>>> print(result)
>>> -10

```
# Versions
We use a modified version of Semantic Versioning for all changes. See version strategy for details which is effective from 2 Nov 2023. 

## Project Statistics and Contributions
[![GitHub stars](https://img.shields.io/github/stars/username/repo.svg?style=social&label=Stars)](https://github.com/username/repo)

You can view statistics for this project on [Libraries.io](https://libraries.io/) or check out our [GitHub repository](https://github.com/your-username/your-repository) for more detailed insights. We welcome contributions, bug reports, and feature requests. Feel free to open issues or submit pull requests on GitHub!


## Supported Version

Only the current MAJOR version of SDK is supported. New features, functionality, bug fixes, and security updates will only be added to the current MAJOR version.

A current release is on the leading edge of our SDK development, and is intended for customers who are in active development and want the latest and greatest features.  Instead of stating a release date for a new feature, we set a fixed minor or patch release cadence of maximum 2-3 months (while we may release more often). At the same time, there is no schedule for major or breaking release. Instead, we will communicate one quarter in advance the upcoming breaking change to allow customers to plan for the upgrade. We always recommend that all users run the latest available minor release for whatever major version is in use. We highly recommend upgrading to the latest SDK major release at the earliest convenient time and before the EOL date.


# Copyright and License

    Copyright (c) 2018 The Python Packaging Authority

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.