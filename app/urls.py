from django.urls import include, path
from . import views


app_name="post"


urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('all-posts/', views.AllPostView.as_view(), name='all_posts'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('like/', views.like, name='like'),
    path("search/", views.SearchResultsView.as_view(), name="search_results"),
    path('create/', views.create, name='post-create'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/update', views.update_view, name="post_update" ),
    path('<slug:slug>/delete', views.PostDeleteView.as_view(), name="post_delete" ),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
]