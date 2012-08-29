###################
django-tastypie-ext
###################

A collection of lightweight, reusable extensions (models, resources and backends) for use with [django-tastypie](http://www.github.com/toastdriven/django-tastypie).

Overview
========
**django-tastypie-ext** encapsulates a set of functionalities and resources
that are often needed in practice, and are not part of the core tastypie package.
Some of these also rely on other 3rd party django extensions but for the most part an attempt has been made to keep it as lean as possible with respect to external dependencies.


Features
========
Authentication Backends
------------------------
* **FacebookOAUTH2Authentication** - Authenticate with Facebook's Graph API using OAuth 2.0. This uses the excellent [Django-facebook](https://github.com/tschellenbach/Django-facebook) package.

Reusable Resources
------------------
* **POSTAPITokenAuthenticationResource** - Given a user's credentials (username/password), create a session token and return it. This allows for token-based  session management/authentication in a RESTful API. This is based on the ApiTokenAuthentication backend introduced in [this django-tastypie fork](https://github.com/toastdriven/django-tastypie/pull/315). 
* **GETAPITokenAuthenticationResource** - Similar to *POSTAPITokenAuthenticationResource*, but supports HTTP GET. While strictly speaking, the creation of a token is logically a POST operation (e.g creating a new resource), in many real-world scenarios its useful to be able to perform this using HTTP GET.
* **GETAPIFacebookTokenAuthenticationResource** - Authenticates a user given a facebook access token. This will verify token is valid by hitting the facebook graph API, and then will fetch the corresponding Django User associated with the facebook user. If none already exists, it will create a new one. Upon successful authentication, this will return a new token to be used with subsequent calls to the RESTful API, as well as information about the (new/existing) user associated with the facebook account. This is very useful for the somewhat complex scenario of creating a mobile app, using facebook connect/graph api as well as a RESTful backend API.

Examples
========
See the ./examples directory for usage examples


Installation
============
* Checkout the git source code and run *setup.py install* to install the python package. 
* Once installed, add it to your INSTALLED_APPS by including 'tastypie_ext'.
You should also have already included any dependent app (e.g 'tastypie') in your INSTALLED_APPS.
* Thats it. See examples section for where to take it from this point.

