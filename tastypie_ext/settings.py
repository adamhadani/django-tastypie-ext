from django.conf import settings

# Fields to return for the API UserResource
TASTYPIE_EXT_USERRESOURCE_FIELDS = getattr(settings, 'TASTYPIE_EXT_USERRESOURCE_FIELDS', 
                                ['username', 'first_name', 'last_name', 'email'])

