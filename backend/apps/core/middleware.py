# django modules
from django.conf import settings 
from django.utils import translation,timezone 
import pytz

class LanguageAndTimezoneMiddleware:
    """
    Middleware that:
    1. Detects and activates the correct language per request
    2. Activates the user's timezone if authenticated
    
    Language priority:
    1. Authenticated user's preferred_language
    2. ?lang= query parameter
    3. Accept-Language HTTP header
    4. Default (settings.LANGUAGE_CODE = 'en')
    """

    def __init__(self,get_response):
        self.get_response = get_response
    

    def __call__(self,request):
        lang = self._resolve_language(request)
        translation.activate(lang)
        request.LANGUAGE_CODE=lang 

        # Activate user timezone 
        self._activate_timezone(request)

        response =self.get_response(request)

        #deactivate after response 
        translation.deactivate()
        timezone.deactivate()
        return response 
    



    def _resolove_language(self,request):
        supported = settings.SUPPORTED_LANGUAGES
        # first check the  user's saved language 
        
        if request.user.is_authenticated:
            lang = getattr(request.user, "preferred_language", None)
            if lang in supported:
                return lang
            
        
        #get by the link query parameters 
        lang = request.GET.get("lang")
        if lang in supported:
            return lang
        

        # 3 ACCEPT-LANGUAGE header 
        accept = request.META.get("HTTP_ACCEPT_LANGUAGE", "")
        for part in accept.split(","):
            code = part.strip().split(";")[0].strip()[:2]
            if code in supported:
                return code
            
        
        return settings.LANGUAGE_CODE 
    

    def _activate_timezone(self, request):
        if request.user.is_authenticated:
            tz_name = getattr(request.user, "timezone", "UTC")
            try:
                tz = pytz.timezone(tz_name)
                timezone.activate(tz)
                return
            except pytz.exceptions.UnknownTimeZoneError:
                pass
        timezone.activate(pytz.utc)