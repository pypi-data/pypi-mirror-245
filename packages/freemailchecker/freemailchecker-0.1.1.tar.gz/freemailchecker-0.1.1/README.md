# freemailchecker
Small python package which checks for free or disposable email addresses from a pre-compiled list

Includes gmail.com style free email addresses and mailinator style disposable
addresses.

# Installing

```bash
pip install freemailchecker
```

# Usage

```python

>>> from freemailchecker import check_free_email, check_free_domain

>>> check_free_email('test@gmail.com')
True
>>> check_free_email('test@google.com')
False
>>> check_free_domain('hotmail.com')
True
>>> check_free_domain('microsoft.com')
False 
```

# Contributions

Contributions to the project or list of domains are very welcome. Please issue
a PR.

The list of domains are in `src/freemailchecker/data/freemaildomains.csv`

# Licence

This code is released under an MIT licence.

# Author

Author is Philip Reynolds. First name dot last name at gmail.com.
