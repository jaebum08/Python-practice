from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "main_app/index.html")

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/')
    hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hashpw)
    request.session['logged_in'] = True
    request.session['user_id'] = user.id
    return redirect('/quotes')

def login(request):
    print(request.POST)
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, key)
        return redirect('/')
    user = User.objects.filter(email = request.POST['email'])
    request.session['logged_in'] = True
    request.session['user_id'] = user[0].id
    return redirect('/quotes')

def quotes(request):
    if not 'logged_in' in request.session:
        return redirect('/')

    context = {
        'all_quotes':Quote.objects.all(),
        'user': User.objects.get(id = request.session['user_id']),
        # 'total_likes': Quote.objects.get(id=).liked_users.all().count
    }
    return render(request,"main_app/success.html",context)

def log_out(request):
    del request.session['user_id']
    del request.session['logged_in']
    return redirect('/')
# end login and registration 

def add_quotes(request):
    if not 'logged_in' in request.session:
        return redirect('/')
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, key)
        return redirect('/quotes')
    user = User.objects.get(id = request.session['user_id'])
    quote = Quote.objects.create(author = request.POST['author'],quote = request.POST['quote'], uploaded_by = user)
    print(quote)
    return redirect('/quotes')

def user_index(request,user_id):
    if not 'logged_in' in request.session:
        return redirect('/')
    context = {
        'user':User.objects.get(id = user_id),
        'quotes':Quote.objects.filter(uploaded_by =user_id)
    }
    return render(request,"main_app/user.html",context)

def myaccount_index(request,user_id):
    if not 'logged_in' in request.session:
        return redirect('/')
    user_id = request.session['user_id']
    context = {
        'user':User.objects.get(id = user_id),
    }

    return render(request,"main_app/account.html",context)

def edit_account(request,user_id):
    if not 'logged_in' in request.session:
        return redirect('/')
    errors = User.objects.edit_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags =key)
        return redirect('/myaccount/'+str(user_id))
    user = User.objects.get(id = user_id)
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.save()
    return redirect('/quotes')

def delete(request,quote_id):
    if not 'logged_in' in request.session:
        return redirect('/')
    quote = Quote.objects.get(id = quote_id)
    quote.delete()
    return redirect ('/quotes')

def like(request,quote_id):
    if not 'logged_in' in request.session:
        return redirect('/')
    quote = Quote.objects.get(id = quote_id)
    user = User.objects.get(id = request.session['user_id'])
    user.liked_quote.add(quote)
    return redirect ('/quotes')


