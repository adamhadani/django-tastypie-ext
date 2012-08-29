from tastypie.api import Api


v1_api = Api(api_name='v1')

# Register your own API resources
from myapp.resources import MyAppAPIResource
v1_api.register(MyAppAPIResource)


# Register tastypie_ext's GET-based APIToken authentication
from tastypie_ext.resources import GETAPITokenAuthenticationResource
v1_api.register(GETAPITokenAuthenticationResource())
"""
Can now be used, e.g:

http://<user>:<pass>@mysite.com/api/v1/authenticate

Will return a token that can then be used with Resources 
using the ApiTokenAuthentication authentication backend.

"""


# Register tastypie_ext's GET-based Facebook access_token authentication
from tastypie_ext.resources import GETAPIFacebookTokenAuthenticationResource
v1_api.register(GETAPIFacebookTokenAuthenticationResource())
"""
Can now be used, e.g:

http://mysite.com/api/v1/fb_authenticate?access_token=<FB_ACCESS_TOKEN>

If token is valid, this will create and/or login the application user and
return a valid token to be used with subsequent Resources using the ApiTokenAuthentication 
authentication backend. 
"""

# Your URL mapping...
urlpatterns = patterns('',
    # API
    (r'^api/', include(v1_api.urls)),
)
