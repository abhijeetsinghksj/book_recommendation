# urls.py
from django.urls import path
from books import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('recommendations/submit/', views.submit_recommendation, name='submit_recommendation'),
    path('', views.search_results, name='search_results'),
    path('recommendations/', views.interactive, name='recommendations'),
    path('recommendations/<int:recommendation_id>/', views.get_recommendation_by_id, name='get_recommendation_by_id'),
    path('recommendations/filter/', views.filter_recommendations, name='filter_recommendations'),
    path('recommendations/like/<int:recommendation_id>/', views.like_recommendation, name='like_recommendation'),
    path('recommendations/comment/<int:recommendation_id>/', views.comment_recommendation, name='comment_recommendation'),
    path('books/search/', views.search_books, name='search_books'),
    path('books/submit/', views.submit_recommendation, name='submit_recommendation'),  # Make sure this is correct
    path('recommendations/all/', views.get_all_recommendations, name='get_all_recommendations'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('dynamic-filter/', views.dynamic_filter, name='dynamic_filter'),
    path('personal-recommendations/', views.personal_recommendations, name='personal_recommendations'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('books/filter/', views.filter_books, name='filter_books'),
    path('books/delete/<int:recommendation_id>/', views.delete_recommendation, name='delete_recommendation'),
    path('fetch/', views.get_recommendations, name='get_recommendations'),
]
