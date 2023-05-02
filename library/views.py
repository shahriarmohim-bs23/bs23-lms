from .models import Category, Book, Review, Copy, Borrow
from .forms import BookForm, CategoryForm, CopyForm
from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .filter import FilterBooks
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views import View
# def add_book(request):
#     if request.method == 'POST':
#         form = BookForm(request.POST, request.FILES)
#         if form.is_valid():
#             book = form.save()
#             return redirect('library:book_added')
#     else:
#         form = BookForm()
#     return render(request, 'pages/add_book.html', {'form': form})


# def add_category(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             category = form.save()
#             return redirect('library:book_added')
#     else:
#         form = CategoryForm()
#     return render(request, 'pages/add_category.html', {'form': form})

# def add_copy_form(request):
#     if request.method == 'POST':
#         form = CopyForm(request.POST)
#         if form.is_valid():
#             book = form.cleaned_data.get('book')
#             copy = form.cleaned_data.get('copy')
#             add_copy(request, book, copy)
#             if not book.in_stock:
#                 book.in_stock = True
#                 book.save()
#             return redirect('library:book_added')
#     else:
#         form = CopyForm()

#     return render(request, 'pages/add_copy.html', {'form': form})

# class CategoriesView(View):
#     def get_context_data(self):
#         context = {}
#         context['categories'] = Category.objects.all()
#         return context 


# def all_books(request):
#     books = Book.objects.all()
#     paginator = Paginator(books, 4)
#     page_number = request.GET.get('page')
#     books = paginator.get_page(page_number)
#     context = {'products': books}
#     return render(request, 'pages/view_book_list.html', context )

# def borrowed_copy(request):
#     borrowed_copy = Borrow.objects.filter(borrower=request.user)
#     paginator = Paginator(borrowed_copy, 4)
#     page_number = request.GET.get('page')
#     borrowed_copy = paginator.get_page(page_number)
#     context = {'borrowed_copies': borrowed_copy}
#     return render(request, 'pages/borrowed_copy.html', context)


# def owned_copy(request):
#     owned_copies = Copy.objects.filter(owner=request.user)
#     paginator = Paginator(owned_copies, 4)
#     page_number = request.GET.get('page')
#     owned_copies = paginator.get_page(page_number)
#     context = {'owned_copies': owned_copies}
#     return render(request, 'pages/owned_copy.html', context)



# def category_list(request, category_slug=None):
#     category = get_object_or_404(Category, slug=category_slug)
#     books = Book.objects.filter(category=category)
#     return render(request, 'pages/view_book_list.html', {'category': category, 'products': books})

def categories(request):
    return {
        'categories': Category.objects.all()
    }
class AddItemView(FormView):
    success_url = reverse_lazy('library:book_added')
    form_class = None

    def get_form_class(self):
        return self.form_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    
    def get_template_names(self):
        return [f'{self.template_name}']


    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

class BookAddedView(TemplateView):
    template_name = 'pages/book_added.html'

class PaginatedListView(ListView):
    paginate_by = 4
    context_object_name = 'data'

    def get_queryset(self):
        queryset = super().get_queryset()
        path = self.request.path
        if path == '/owned_copy/':
            return Copy.objects.filter(owner=self.request.user)
        elif path == '/borrowed_copy/':
            return Borrow.objects.filter(borrower=self.request.user)
        else:
            return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page')
        paginator = Paginator(context[self.context_object_name], self.paginate_by)
        context[self.context_object_name] = paginator.get_page(page_number)
        return context



class AllBooksView(PaginatedListView):
    model = Book
    template_name = 'pages/view_book_list.html'
    context_object_name = 'products'
   

class BorrowedCopyView(PaginatedListView):
    model = Borrow
    template_name = 'pages/borrowed_copy.html'
    context_object_name = 'borrowed_copies'

class OwnedCopyView(PaginatedListView):
    model = Copy
    template_name = 'pages/owned_copy.html'
    context_object_name = 'owned_copies'



def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    reviews = book.reviews.all()
    paginator = Paginator(reviews, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        content = request.POST.get('content', '')
        rating = request.POST.get('rating')
        if content:
            review = Review.objects.create(
                book=book,
                content=content,
                rating=rating,
                user=request.user

            )
            messages.success(request, 'Review added successfully!')
            return redirect('library:book_detail', slug=book.slug)

    return render(request, 'pages/books/detail.html', {'product': book, 'page_obj': page_obj})


def add_copy(request, book, qty):
    count = book.copies.count()

    qty += 1
    for i in range(1, qty):
        Copy.objects.create(book=book, copy=i + count, owner=request.user, status='available')





def borrow_copy(request, slug):
    book = get_object_or_404(Book, slug=slug)
    existing_borrow = Borrow.objects.filter(copy__book=book, borrower=request.user, return_date__isnull=True).first()
    if existing_borrow:
        return render(request, 'pages/books/detail.html',
                      {'product': book, 'msg': "You have already borrowed a copy of this book."})
    for copy in book.copies.all():
        if copy.status == 'available':
            copy.status = 'borrowed'
            copy.save()
            Borrow.objects.create(copy=copy, borrower=request.user)
            return render(request, 'pages/books/detail.html',
                          {'product': book, 'msg': "Successfully Borrowed the copy"})
    return render(request, 'pages/books/detail.html', {'product': book, 'msg': "There is no available copy"})





def search_books(request):
    books = Book.objects.all()
    filters = FilterBooks(request.GET, queryset=books)
    filtered_books = filters.qs
    return render(request, 'pages/books/searchbooks.html',
                  {'filters': filters, 'Books': filtered_books})