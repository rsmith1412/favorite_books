from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Book
import bcrypt

# Create your views here.
def index(request):
    return render(request, "fav_books/index.html")

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='reg')
        return redirect("/")
    else:
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        pw = request.POST["password"]
        pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
        new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
        request.session["user_id"] = new_user.id
        return redirect("/books")

def login(request):
    email = request.POST["email"]
    pw = request.POST["password_login"]
    users = User.objects.filter(email = email)
    if len(users) == 0:
        messages.error(request, "Invalid login.", extra_tags='login')
        return redirect("/")

    user = users[0]
    if bcrypt.checkpw(pw.encode(), user.password.encode()):
        request.session["user_id"] = user.id
        return redirect("/books")
    messages.error(request, "Invalid login.", extra_tags='login')
    return redirect("/")

def books(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session["user_id"])
        books = Book.objects.all()
        context = {
            "user" : user,
            "books" : books
        }
        return render(request, "fav_books/all_books.html", context)
    return redirect("/")

def add_book(request):
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='book')
        return redirect("/books")
    else:
        user = User.objects.get(id=request.session["user_id"])
        title = request.POST["title"]
        desc = request.POST["desc"]
        book = Book.objects.create(title=title, description=desc, uploaded_by=user)
        book.users_who_like.add(user)
        return redirect("/books")

def show_book(request, id):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session["user_id"])
        book = Book.objects.get(id=id)
        context = {
            "user" : user,
            "book" : book
        }
        return render(request, "fav_books/show_book.html", context)
    return redirect("/")

def edit_book(request, id):
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='update')
        return redirect("/books/" + id)
    else:
        book = Book.objects.get(id=id)
        book.title = request.POST["title"]
        book.description = request.POST["desc"]
        book.save()
        return redirect("/books/" + id)

def favorite(request, id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=id)
    book.users_who_like.add(user)
    return redirect("/books/" + id)

def unfavorite(request, id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=id)
    book.users_who_like.remove(user)
    return redirect("/books/" + id)

def delete_book(request, id):
    Book.objects.get(id=id).delete()
    return redirect("/books")

def logout(request):
    request.session.clear()
    return redirect("/")