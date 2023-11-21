import requests

from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import SearchBookForm, AddBookForm


def home(request):
    """
    display a search form to search books
    display 10 books searched
    api - https://www.googleapis.com/books/v1/volumes?q={search terms}
    """
    if request.method == "POST":
        form = SearchBookForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data.get("text")

            url = f"https://www.googleapis.com/books/v1/volumes?q={text}"
            response = requests.get(url)
            data = response.json()

            books = []
            for item in data["items"]:
                volume_info = item['volumeInfo']
                book = {
                    'title': volume_info.get('title'),
                    'subtitle': volume_info.get('subtitle'),
                    'description': volume_info.get('description'),
                    'count': volume_info.get('pageCount'),
                    'categories': volume_info.get('categories'),
                    'rating': volume_info.get('averageRating'),
                    'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail'),
                    'preview': volume_info.get('previewLink')
                }

                books.append(book)

            return render(request, "book/home.html", {
                "title": "books",
                "books": books,
                "form": form
            })

    else:
        form = SearchBookForm()

    return render(request, "book/home.html", {
        "title": "books",
        "form": form
    })


def books(request):
    """add a book to the portal"""
    if request.method == "POST":
        form = AddBookForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            messages.success(request, "New book added")
            return redirect("book:home")
    else:
       form = AddBookForm()
    
    return render(request, "book/books.html.html", {
        "title": "books",
        "form": form
    })