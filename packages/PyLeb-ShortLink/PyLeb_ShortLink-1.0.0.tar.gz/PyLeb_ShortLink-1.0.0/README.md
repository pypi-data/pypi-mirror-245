  PyLeb_ShortLink Documentation

PyLeb_ShortLink Documentation
==============================

Overview
--------

PyLeb_ShortLink is a Python library designed for URL shortening using the TinyURL API.

Installation
------------

Install PyLeb_ShortLink using pip:

    pip install PyLeb_ShortLink

Quick Start
-----------

    import shortlink
    
    # Shorten a URL
    shortened_url = shortlink.short("https://example.com")
    
    print("Shortened URL:", shortened_url)
        

License
-------

PyLeb_ShortLink is distributed under the [New Global License Version 3.0 (NewGBLv3)](https://opensource.org/licenses/NewGBL-3.0).

API Reference
-------------

### `short(Link: str) -> str`

Shortens the given URL using the TinyURL API.

#### Parameters:

*   **Link** (str): The URL to be shortened.

#### Returns:

*   **str**: The shortened URL.

If the URL cannot be shortened, the function returns a message indicating the failure.

Dependencies
------------

*   **requests**: Used for making HTTP requests.

Contribution
------------

Contributions, bug reports, and feature requests are welcome on [GitHub](https://github.com/mesteranas/PyLeb_ShortLink).

Contact
-------

For inquiries or support, please contact the author:

*   **Author:** mesteranas
*   **Email:** anasformohammed@gmail.com