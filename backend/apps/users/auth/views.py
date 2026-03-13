# Python modules
from typing import Any
import logging
import pytz

# Third-party modules
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response as DRFResponse
from rest_framework.request import Request as DRFRequest
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.decorators import action
from django.utils.translation import gettext_lazy as _


from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


# Project modules
from apps.users.auth.serializers import RegistrationSerializer, LoginSerializer
from apps.abstract.ratelimit import ratelimit, get_client_ip

logger = logging.getLogger(__name__)


class AuthViewSet(ViewSet):
    """
    ViewSet for Authentication
    """

    permission_classes = [AllowAny]

    @action(
        methods=("POST",),
        detail=False,
        url_path="token",
        url_name="token",
    )
    @ratelimit(key_func=lambda r: get_client_ip(r), rate="10/m", method="POST")
    def login(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> DRFResponse:
        email = request.data.get("email", "N/A")
        logger.info(f"Login attempt: email={email}")

        serializer = LoginSerializer(
            data=request.data,
            context={"request": request},
        )

        if serializer.is_valid():
            logger.info(f"Login successful: email={email}")
            return DRFResponse(
                data=serializer.validated_data,
                status=HTTP_200_OK,
            )

        logger.warning(f"Login failed: email={email}, errors={serializer.errors}")
        return DRFResponse(
            data=serializer.errors,
            status=HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=("POST",),
        detail=False,
        url_path="register",
        url_name="register",
    )
    @ratelimit(key_func=lambda r: get_client_ip(r), rate="5/m", method="POST")
    def register(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> DRFResponse:
        email = request.data.get("email", "N/A")
        logger.info(f"Registration attempt: email={email}")

        serializer: RegistrationSerializer = RegistrationSerializer(
            data=request.data,
            context={"request": request},
        )

        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"Registration successful: user_id={user.id}, email={email}")
            return DRFResponse(
                data=serializer.data,
                status=HTTP_201_CREATED,
            )
        logger.warning(f"Registration failed: email={email}, errors={serializer.errors}")
        return DRFResponse(
            data=serializer.errors,
            status=HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=("POST",),
        detail=False,
        url_path="token/refresh",
        url_name="refresh",
    )
    def token(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> DRFResponse:
        logger.info("Token refresh attempt")
        serializer: TokenRefreshSerializer = TokenRefreshSerializer(
            data=request.data,
        )
        try:
            if serializer.is_valid():
                logger.info("Token refresh successful")
                return DRFResponse(
                    data=serializer.validated_data,
                    status=HTTP_200_OK,
                )
        except TokenError as e:
            logger.error(f"Token refresh failed: {str(e)}")
            raise InvalidToken(e.args[0])

        logger.warning(f"Token refresh validation failed: {serializer.errors}")
        return DRFResponse(
            data=serializer.errors,
            status=HTTP_400_BAD_REQUEST,
        )
    


    @action(
        methods=("PATCH",),
        detail=False,
        url_path="language",
        url_name="language",
        permission_classes=(IsAuthenticated,),
    )
    def set_language(
        self,
        request:DRFRequest,
        *args,
        **kwargs,
    )->DRFResponse:
        """PATCH /api/auth/language -сохранить язык пользователя"""
        from django.conf import settings 

        lang = request.data.get("language")
        
        if lang not in settings.SUPPORTED_LANGUAGES:
            return DRFResponse(
                {"detail":_("Invalid language.Choose from:en,ru,kk")},
                status=HTTP_400_BAD_REQUEST,
            )

        request.user.preferred_language = lang
        request.user.save(update_fields=["preferred_language"])


        logger.info(f"Langage updated:user_id={request.user.id},lang={lang}")
        return DRFResponse(
            {"detail":_("Language updated succesfully."),"language":lang},
            status=HTTP_200_OK,
        )
    

    @action(
        methods =("PATCH",),
        detail = False,
        url_path ="timezone",
        url_name ="timezone",
        permission_classes=(IsAuthenticated,),
    )
    def set_timezone(
        self,
        request:DRFRequest,
        *args,
        **kwargs,
    )->DRFResponse:
        """PATCH /api/auth/timezone -сохранить часовой пояс пользователя"""
        from django.conf import settings 

        tz_name = request.data.get("timezone")
        
        if not tz_name:
            return DRFResponse(
                {"detail":_("Invalid timezone")},
                status=HTTP_400_BAD_REQUEST,
            )
        try:
            pytz.timezone(tz_name)

        except pytz.exceptions.UnknownTimeZoneError:
            return DRFResponse(
                {"detail":_("Invalid timezone")},
                status=HTTP_400_BAD_REQUEST,
            )
        request.user.timezone = tz_name
        request.user.save(update_fields=["timezone"])

        logger.info(f"Timezone updated: user_id={request.user.id}, timezone={tz_name}")
        return DRFResponse(
        {"detail": _("Timezone updated successfully."), "timezone": tz_name},
        status=HTTP_200_OK,
    )