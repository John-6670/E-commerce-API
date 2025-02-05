from django.utils.text import slugify

def generate_unique_slug(instance, field_name='name', slug_field='slug'):
    """
    Generate a unique slug for a Django model instance.

    :param instance: The model instance.
    :param field_name: The field to generate the slug from (default: 'name').
    :param slug_field: The slug field name (default: 'slug').
    :return: A unique slug string.
    """
    base_slug = slugify(getattr(instance, field_name))
    slug = base_slug
    model_class = instance.__class__
    counter = 1

    while model_class.objects.filter(**{slug_field: slug}).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug
