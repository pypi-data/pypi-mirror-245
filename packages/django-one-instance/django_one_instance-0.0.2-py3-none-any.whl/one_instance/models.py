import logging

from django.db import models
from django.conf import settings

logger = logging.getLogger(__name__)

class SingletonModelAlreadyExists(Exception):

    pass

class SingletonModelQuerySet(models.QuerySet):

    DJANGO_ONE_STRICT_DEFAULT = True
    _get_strict_error_msg = 'You should use get() method without any arguments'

    @property
    def _strict(self):
        return getattr(settings, 'DJANGO_ONE_STRICT', 
                       self.DJANGO_ONE_STRICT_DEFAULT)

    def get_instance(self):
        instance = super().last()
        if instance is None:
            raise self.model.DoesNotExist
        return instance

    def get(self, *args, **kwargs):
        if len(args) > 0 or len(kwargs) > 0:
            if self._strict:
                raise TypeError(
                    f'{self._get_strict_error_msg}. Set DJANGO_ONE_STRICT=False '
                    'if you want to silently drop the unneeded arguments.')
            else:
                logger.warning(self._get_strict_error_msg)
        return self.get_instance()

    def create(self, **kwargs):
        if self.count() > 0:
            if self._strict:
                raise SingletonModelAlreadyExists(
                    'You are receiving this error after attempting to create another '
                    'instance of the singleton model. Set DJANGO_ONE_STRICT=False '
                    'to drop the exception and return the model instance instead.')
            logger.warning('model instances already exist, returning last instance')
            return self.get_instance()

        obj = super().create(**kwargs)
        logger.debug(f"created object with pk {obj.pk}")
        return obj
    
    def first(self):
        return self.last()

    def last(self):
        try:
            return self.get_instance()
        except self.model.DoesNotExist:
            return None
        


    #########################
    # NOT SUPPORTED METHODS #
    #########################

    aggregate   = None
    bulk_create = None
    bulk_update = None
    in_bulk     = None


class SingletonModelManager(models.Manager):

    def get_queryset(self):
        qs = super().get_queryset().order_by('-pk')[0:1]
        return super().get_queryset().filter(pk__in=qs)
    

class SingletonModel(models.Model):

    objects = SingletonModelManager.from_queryset(SingletonModelQuerySet)()

    class Meta:
        abstract = True
        
