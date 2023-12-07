# drf-privatbank
This module provides quick integration of the Privatbank API for applications in the Django REST Framework.

## Installation
This framework is published at the PyPI, install it with pip:

    pip install drf_privatbank

Django REST Framework application, you need to install and configure drf_privatbank. To get started, add the following packages to INSTALLED_APPS:

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'drf_privatbank',
    ]

Include social auth urls to your urls.py:

    if settings.ENABLE_PRIVATBANK:
    urlpatterns = [
        ...
        path('privatbank/', include('drf_privatbank.urls', namespace='drf_privatbank')),
    ]

## Usage
1. First, install the "Autoclient" module of the "Privat24 for Business" complex designed to serve corporate clients and private entrepreneurs."Autoclient" is software that allows you to set up periodic automatic receipt of statements / account balances and import payments into Privat24.
2. Finally, use this token and your account's iban to retrieve your personal data and create payments.
