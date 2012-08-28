from django.contrib.auth.models import User          
from django.conf.urls.defaults import url

from tastypie import http
from tastypie import fields
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource, Resource
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization

# These are based on the tastypie fork
from tastypie.models import ApiToken
from tastypie.authentication import ApiTokenAuthentication

class GETAPITokenAuthenticationResource(ModelResource):
    """HTTP GET-based authentication end point
    for use with the ApiTokenAuthentication
    flow. This allows to use this with cross-domain
    AJAX (e.g JSONP)"""
    
    user = fields.ToOneField(
        'api.resources.UserResource', 'user', full=True)
    
    class Meta(object):
        queryset = ApiToken.objects.all()
        resource_name = 'authenticate'
        fields = ['user', 'token']
        allowed_methods = ['get']
        authorization = Authorization()
        authentication = BasicAuthentication()
        
    def prepend_urls(self):
        """We override this to change default behavior
        for the API when using GET to actually "create" a resource,
        in this case a new session/token."""
        
        return [
            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()), 
                self.wrap_view('_create_token'), name="api_get_token"),
            ]
  
    def _create_token(self, request, **kwargs):
        """Validate using BasicAuthentication, and create Api Token
        if authenticated"""
        print "asdf"
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        
        bundle = self.build_bundle(obj=None, request=request)
        bundle = self.obj_create(bundle, request, **kwargs)
        bundle = self.full_dehydrate(bundle)

        self.log_throttled_access(request)
        return self.create_response(request, bundle.data)
    
        
    def obj_create(self, bundle, request=None, **kwargs):
        """Create a new token for the session"""
        bundle.obj = ApiToken.objects.create(user=request.user)
        return bundle
    
    def obj_get(self, request=None, **kwargs):
        raise ImmediateHttpResponse(response=http.HttpUnauthorized())
    
    def obj_get_list(self, request=None, **kwargs):
        raise ImmediateHttpResponse(response=http.HttpUnauthorized())

        
