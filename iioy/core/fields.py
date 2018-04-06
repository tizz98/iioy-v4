from django.db import models
from django.utils.text import slugify


class SlugField(models.SlugField):
    def __init__(self, slug_field, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug_field = slug_field

    def pre_save(self, model_instance, add):
        slug = getattr(model_instance, self.attname)

        if not slug:
            slug = slugify(getattr(model_instance, self.slug_field))
            setattr(model_instance, self.attname, slug[:self.max_length])

        return super().pre_save(model_instance, add)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['slug_field'] = self.slug_field
        return name, path, args, kwargs
