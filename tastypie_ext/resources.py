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

import tastypie_ext.settings as settings 

class UserResource(ModelResource):
    """
    Resource to represent an API User.
    Used e.g for authentication. This implementation
    relies on django's inbuilt User model from the `contrib.auth` package.
    
    """
    
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        
        fields = settings.TASTYPIE_EXT_USERRESOURCE_FIELDS
        
        authentication = ApiTokenAuthentication()
        authorization = Authorization()
        
        
class SessionResource(ModelResource):
    """Represent a (active) session.
    Can be used to fetch current user associated
    with session, as well as destroy session (e.g invalidate session token)
    using an HTTP DELETE on the resource URI.
    
    """
    user = fields.ToOneField(
        'tastypie_ext.resources.UserResource', 'user', full=True)

    class Meta(object):
        queryset = ApiToken.objects.all()
        resource_name = 'sessions'
        fields = ['user', 'token']
        allowed_methods = ['get', 'delete']
        authorization = Authorization()
        authentication = ApiTokenAuthentication()
        always_return_data = True
        
        
class POSTAPITokenAuthenticationResource(ModelResource):
    """
    HTTP POST-based authentication end point
    for use with the ApiTokenAuthentication 
    flow.
    
    """
    
    user = fields.ToOneField(
        'tastypie_ext.resources.UserResource', 'user', full=True)

    class Meta(object):
        queryset = ApiToken.objects.all()
        resource_name = 'authenticate'
        fields = ['user', 'token']
        allowed_methods = ['post']
        authorization = Authorization()
        authentication = BasicAuthentication()
        always_return_data = True

    def obj_create(self, bundle, request=None, **kwargs):
        " Create a new token for the session."
        bundle.obj = ApiToken.objects.create(user=request.user)
        return bundle

    def dehydrate_resource_uri(self, bundle):
        return SessionResource().get_resource_uri(bundle.obj)



class GETAPITokenAuthenticationResource(ModelResource):
    """
    HTTP GET-based authentication end point
    for use with the ApiTokenAuthentication
    flow. This allows to use this with cross-domain
    AJAX (e.g JSONP).
    
    """
    
    user = fields.ToOneField(
        'tastypie_ext.resources.UserResource', 'user', full=True)
    
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
        print request
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

        
