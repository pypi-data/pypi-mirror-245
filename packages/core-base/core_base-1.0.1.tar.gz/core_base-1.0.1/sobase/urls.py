"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path, include, re_path
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from sobase import dispatch
from sobase import settings
from core_base.system.views.dictionary import InitDictionaryViewSet
from core_base.system.views.login import (
    LoginView,
    CaptchaView,
    LogoutView, CustomTokenRefreshView,
)
from core_base.system.views.system_config import InitSettingsViewSet

# =========== 初始化系统配置 =================
dispatch.init_system_config()
dispatch.init_dictionary()
# =========== 初始化系统配置 =================
urlpatterns = (
        [
            path("sobase/api/system/", include("core_base.system.urls")),
            path("sobase/api/login/", LoginView.as_view(), name="token_obtain_pair"),
            path("sobase/api/logout/", LogoutView.as_view(), name="token_obtain_pair"),
            path("sobase/api/token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
            path("sobase/api/captcha/", CaptchaView.as_view()),
            path("sobase/api/init/dictionary/", InitDictionaryViewSet.as_view()),
            path("sobase/api/init/settings/", InitSettingsViewSet.as_view()),
        ]
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
        + [re_path(ele.get('re_path'), include(ele.get('include'))) for ele in settings.PLUGINS_URL_PATTERNS]
)
