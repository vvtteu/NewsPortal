from django.urls import path
from .views import *

urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', SearchPosts.as_view(), name='search'),
   path('create/news/', NewsCreate.as_view(), name='news_create'),
   path('create/article/', ArticleCreate.as_view(), name='articles_create'),
   path('article/<int:pk>/edit/', ArticleUpdate.as_view(), name='articles_edit'),
   path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='articles_delete'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('upgrade/', upgrade_me, name='upgrade_me'),
   path('lk/', personal_account_view, name='lk'),
   path('subscribe/', subscribe_to_category, name='subscribe'),
]
