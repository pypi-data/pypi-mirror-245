jk_mediawikiapi
==========

Introduction
------------

This python module provides access to a MediaWiki wiki via its API.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/python-module-jk-mediawikiapi)
* [pypi.python.org](https://pypi.python.org/pypi/jk_mediawikiapi)

Why this module?
----------------

The author of this module needed to access a MediaWiki and retrieve and update some data. At that point time quite python modules were available for this purpose and the author of this module experimente with quite some of these modules. To his suprprise none of these modules worked with his installation of a quite recent MediaWiki installation. After spending quite some time in trying to use existing modules to avoid the rework involved in the process of implementing functionality again without sufficient success, he had no other choice as to implement his own MediaWiki client himself. That's how this module came into existance.

This module aims to provide a *working* MediaWiki access for at least the most frequent functionality.

Limitations of this module
--------------------------

You *can* use this module for production *iff* you do some testing in your usecase.

Nevertheless this module is still considered of being "alpha". That implies:

1. There might be some API changes in the future. Methods might get renamed or method arguments might get renamed.
	* Nevertheless if you update to a more recent version of this module and find things broken it should not be difficult to find out possible changes in method and method argument names and update your own code accordingly.
2. There might be some special situations in responses of servers that might not yet have taken into consideration in the implementation of this module.
	* In the unlikely case that you encounter such a situation either ...
		a) ... fix this problem yourself and then send the code to the author of this module for integration, or
		b) ... contact the author of this module directly, provide details about the problem and he'll try to fix that problem as soon as possible.
3. Only the most frequent functionality is provided. There might be some special functionality not yet considered to provide as a method in <c>MediaWikiClient</c>.
	* In that case see (2) how to deal with this situation.

How to use this module
----------------------

### Import this module

Please include this module into your application using the following code:

```python
import jk_mediawikiapi
```

...

Contact Information
-------------------

This work is Open Source. This enables you to use this work for free.

Please have in mind this also enables you to contribute. We, the subspecies of software developers, can create great things. But the more collaborate, the more fantastic these things can become. Therefore Feel free to contact the author(s) listed below, either for giving feedback, providing comments, hints, indicate possible collaborations, ideas, improvements. Or maybe for "only" reporting some bugs:

* Jürgen Knauth: jknauth@uni-goettingen.de, pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



