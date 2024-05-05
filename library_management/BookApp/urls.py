from django.urls import re_path as url
from BookApp import views as views

urlpatterns = [
	url(r'^list/book/$', views.GetAllBooks.as_view(), name='book_list'),
	url(r'^add/book/$', views.AddBook.as_view(), name='book_add'),
	url(r'^add/member/$', views.AddMember.as_view(), name='add_member'),
	url(r'^issue/book/$', views.IssueBook.as_view(), name='book_issue'),
	url(r'^return/(?P<transaction_id>[0-9]+)/book/$', views.ReturnBook.as_view(), name='book_return'),
	url(r'^import/book/$', views.ImportBooks.as_view(), name='book_import'),
	url(r'^search/book/$', views.SearchBooks.as_view(), name='book_search'),
	
] 