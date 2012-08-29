from django.contrib.auth import authenticate, login

from tastypie.authentication import Authentication
from tastypie.http import HttpUnauthorized

class FacebookOAUTH2Authentication(Authentication):
    """
    Handles authentication delegating to Facebook OAuth 2.0,
    using the Django-facebook package.
    
    See tastypie_ext.resources.GETAPIFacebookTokenAuthenticationResource
    for more documentation on the typical flow using this.
    
    """

    def is_authenticated(self, request, **kwargs):
        """
        Authenticate with facebook, and return
        user upon success.
        
        """

        # Make sure user supplied access token in request
        try:
            access_token = request.GET['faccess_token']
        except KeyError:
            return self._unauthorized()

        # Authenticate with facebook
        from open_facebook import OpenFacebook
        from django_facebook.connect import connect_user

        facebook = OpenFacebook(access_token)

        try:
            if not facebook or \
                not facebook.is_authenticated():
                return self._unauthorized()
        except:
            return self._unauthorized()
        
        
        # Facebook authenticated, now associate
        # with own internal user, Creating a new user if 
        # necessary.
        action, user = connect_user(request, access_token, facebook)
        request.user = user
  
        return True
    

    def _unauthorized(self):
        response = HttpUnauthorized()
        return response
        
    