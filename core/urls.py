"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from authors.views import AuthorListCreateView, AuthorDetailView
from books.views import BookListCreateView, BookDetailView
from borrowrecords.views import BorrowRecordCreateView, BorrowRecordReturnView
from reports.views import ReportView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
   openapi.Info(
      title="Library Management System API",
      default_version='v1',
      description="API for Library Management System",
      terms_of_service="https://www.librarymanagementsystem.com/policies/terms/",
      contact=openapi.Contact(email="prashanttomar2000@rediffmail.com.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # Authors Routes
    path('api/authors/', AuthorListCreateView.as_view(), name='author-list-create'),
    path('api/authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    
    # Books Routes
    path('api/books/', BookListCreateView.as_view(), name='book-list-create'),
    path('api/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Borrow Routes
    path('api/borrow/', BorrowRecordCreateView.as_view(), name='borrow-create'),
    path('api/borrow/<int:pk>/return/', BorrowRecordReturnView.as_view(), name='borrow-return'),
    
    # Reports Routes
    path('api/reports/', ReportView.as_view(), name='reports'),
    
    # Swagger Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)