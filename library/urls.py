from django.urls import path

from .import views
from .views import AddItemView,BookAddedView,AllBooksView, BorrowedCopyView, OwnedCopyView
app_name = 'library'
from .forms import BookForm, CategoryForm,CopyForm

urlpatterns = [
    #path('view_all_book/', views.all_books, name='all_books'),
    #path('add/book/',views.add_book,name='add_book'),
    #path('add/category/',views.add_category,name='add_category'),
    #path('add/copy/', views.add_copy_form, name='add_copy'),
    #path('owned/copy/', views.owned_copy, name='owned_books'),
    #path('borrowed/copy/', views.borrowed_copy, name='borrowed_books'),
    #path('search/<slug:category_slug>/', views.category_list, name='category_list'),
    path('add/book/', AddItemView.as_view(form_class=BookForm,template_name='pages/add_book.html'), name='add_book'),
    path('add/category/', AddItemView.as_view(form_class=CategoryForm,template_name='pages/add_category.html'), name='add_category'),
    path('add/copy/', AddItemView.as_view(form_class=CopyForm, template_name='pages/add_copy.html'), name='add_copy'),
    path('book_added/', BookAddedView.as_view(), name='book_added'),
    path('view_all_book/', AllBooksView.as_view(), name='all_books'),
    path('owned/copy/', OwnedCopyView.as_view(), name='owned_books'),
    path('borrowed/copy/', BorrowedCopyView.as_view(), name='borrowed_books'),
    path('category/<slug:category_slug>/', AllBooksView.as_view(), name='category_list'),
    path('item/<slug:slug>/', views.book_detail, name='book_detail'),
    path('borrow/<slug:slug>/', views.borrow_copy, name='borrow_copy'),
    path('searchbooks/', views.search_books, name='search_books'),

]