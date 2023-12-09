PyLeb_CurrencyConverter Documentation

PyLeb_CurrencyConverter Documentation
======================================

Overview
--------

PyLeb_CurrencyConverter is a Python library for converting between different currencies using Google's currency conversion service.

Installation
------------

Install PyLeb_CurrencyConverter using pip:

`pip install PyLeb_CurrencyConverter`

Quick Start
-----------

`from CurrencyConverter import convert   result = convert("USD", "EUR", 100)   print(result)`

API Reference
-------------

### `convert(currency_from, currency_to, amount)`

Converts an amount from one currency to another.

#### Parameters:

*   `currency_from`: Currency code from which the amount needs to be converted.
*   `currency_to`: Currency code to which the amount needs to be converted.
*   `amount`: Amount to be converted.

#### Returns:

Returns result as float.

### `Currencies`

#### Returns:

Returns a dictionary with currency codes as keys and currency names as values.

License
-------

PyLeb_CurrencyConverter is distributed under the [GNU General Public License v3.0](https://opensource.org/licenses/GPL-3.0).

Project Information
-------------------

*   **GitHub Repository:** [PyLeb_CurrencyConverter](https://github.com/mesteranas/PyLeb_CurrencyConverter)
*   **Author:** mesteranas (Email: anasformohammed@gmail.com)