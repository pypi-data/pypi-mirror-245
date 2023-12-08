[![Django CI](https://github.com/federicodabrunzo/django-one-instance/actions/workflows/django.yml/badge.svg?branch=workflow)](https://github.com/federicodabrunzo/django-one-instance/actions/workflows/django.yml)

Django One Instance
===========
Django One Instance is a Django app which enforces the use of a single entry for a given model (i.e.: singleton model). 

The app provides an abstract model to extend which enforces the singleton models behaviour and an admin base class for registering the singleton models in the admin site.

Usage
-----------

Say you have a Config model and you want to enforce its use only with one instance. All you need to to is to extend the SingletonModel abstract model which provides a custom manager for this purpose.

```python
# models.py
from one_instance.models import SingletonModel

class Config(SingletonModel):

    enabled = models.BooleanField()
```

You can also register the model in the django admin and it will be aware that there is only one object.

```python
# admin.py
from django.contrib import admin

from testapp.models import Config
from one_instance.admin import SingletonAdmin


admin.site.register(Config, SingletonAdmin)
```

### New singleton model

```python
from testapp.models import Config
>>> Config.objects.create(enabled=False)
<Config: Config object (1)>
>>> Config.objects.get()
<Config: Config object (1)>
```

Note how you don't have to pass the pk to the get() method. If you try to create another instance you get an error.

```
>>> Config.objects.create(enabled=False)
one_instance.models.SingletonModelAlreadyExists: You are receiving this error after attempting to create another instance of the singleton model. Set DJANGO_ONE_STRICT=False to drop the exception and return the model instance instead.
```

### Pre-existing model
If you extend the SingletonModel for a pre-existing model with many instances, the default get() behaviour is to return the last entry which becames the singleton object.
```
>>> Config.objects.get()
<Config: Config object (3)>
```
the other entries are hidden by the manager
```
>>> Config.objects.all()
<SingletonModelQuerySet [<Config: Config object (3)>]>
>>> Config.objects.first()
<Config: Config object (3)>
>>> Config.objects.last()
<Config: Config object (3)>
```
if you try to forcefully get one of the other instances, you get an error
```
>>> Config.objects.get(pk=1)
TypeError: You should use get() method without any arguments. Set DJANGO_ONE_STRICT=False if you want to silently drop the unneeded arguments.
```

Installation
-----------
- `pip install django-one-instance`
- Add "one_instance" to your INSTALLED_APPS setting like this:
    ```python
    INSTALLED_APPS = [
        ...,
        "one_instance",
    ]
    ```