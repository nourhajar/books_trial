from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
def index(request):
    if 'first_name' in request.session:
        del request.session['first_name']
    return render(request, "favorites/index.html")
def congrats(request):
    if 'first_name' not in request.session:
        return redirect('/')
    else:
        context = {
            "all_books": Book.objects.all(),
            "user": User.objects.get(first_name=request.session['first_name'])
        }
    return render(request, "favorites/congrats.html", context)
def book(request, id):
    context = {
        "book": Book.objects.get(id=id),
        "user": User.objects.get(first_name=request.session['first_name'])
    }
    return render(request, "favorites/book.html", context)
def edit(request, id):
    context = {
        "book": Book.objects.get(id=id),
        "user": User.objects.get(first_name=request.session['first_name'])
    }
    book= Book.objects.get(id=id)
    print("@@@@@@@@@@@", book.users_who_like.all().values())
    return render(request, "favorites/edit.html", context)
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    if request.method == "POST":
        fn = request.POST['first_name']
        request.session['first_name'] = request.POST['first_name']
        ln = request.POST['last_name']
        em = request.POST['email']
        pw = request.POST['password']
        hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
        User.objects.create(first_name=fn, last_name=ln, email=em, password=hash)
        return redirect("/congrats")
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    if request.method == "POST":
        user = User.objects.filter(email = request.POST['email']).values()
        print("************", user)
        request.session['first_name'] = user[0]['first_name']
        return redirect("/congrats")
def add_book(request):
    if request.method == "POST":
        user = User.objects.get(first_name = request.session['first_name'])
        x = request.POST['title']
        y = request.POST['description']
        Book.objects.create(title=x, description=y, uploaded_by=user)
        book = Book.objects.last()
        book.users_who_like.add(user)
        print("***$*$*$*$*$*$*$", book.id)
        id = str(book.id)
        return redirect("/book/" + id)
def update(request, id):
    if request.method == "POST":
        c = Book.objects.get(id=id)
        c.title = request.POST['title']
        c.description = request.POST['title']
        c.save()
        return redirect("/congrats")
def remove_favorite(request, id):
    if request.method == "GET":
        user = User.objects.get(first_name = request.session['first_name'])
        book = Book.objects.get(id=id)
        book.users_who_like.remove(user)
        id = str(book.id)
        return redirect("/book/" + id)
def add_favorite(request, id):
    if request.method == "GET":
        user = User.objects.get(first_name = request.session['first_name'])
        book = Book.objects.get(id=id)
        book.users_who_like.add(user)
        id = str(book.id)
        return redirect("/book/" + id)