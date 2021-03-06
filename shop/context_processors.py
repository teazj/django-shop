# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import __version__
from django.conf import settings
from shop.models.customer import CustomerModel
from shop import settings as shop_settings


def customer(request):
    """
    Add the customer to the RequestContext
    """
    msg = "The request object does not contain a customer. Edit your MIDDLEWARE_CLASSES setting to insert 'shop.middlerware.CustomerMiddleware'."
    assert hasattr(request, 'customer'), msg

    context = {
        'customer': request.customer,
        'site_header': settings.SHOP_APP_LABEL.capitalize(),
    }
    if request.user.is_staff:
        try:
            context.update(customer=CustomerModel.objects.get(pk=request.session['emulate_user_id']))
        except (CustomerModel.DoesNotExist, KeyError, AttributeError):
            pass
    return context


def version(request):
    """
    Add version to context, since in Django-1.9 the path for jquery changed
    """
    return {
        'DJANGO_VERSION': __version__,
    }


def ng_model_options(request):
    """
    Add ng-model-options to the context, since these settings must be configurable
    """
    return {
        'EDITCART_NG_MODEL_OPTIONS': shop_settings.EDITCART_NG_MODEL_OPTIONS,
        'ADD2CART_NG_MODEL_OPTIONS': shop_settings.ADD2CART_NG_MODEL_OPTIONS,
    }
