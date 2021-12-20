
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from datetime import datetime

def index(request):
    # Display top level liked 5 categories in main page
    # get list of 5 categories by order 
    category_list = Category.objects.order_by("-likes")[:5]
    page_list = Page.objects.order_by("-views")[:5]
    context_dic = {
        "categories": category_list,
        "pages": page_list
    }

    request.session.set_test_cookie()

    '''
    context_dic = {
        'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"
    }
    html='Rango says hey there partner! <br\> <a href="/rango/about/">About</a>'
    return HttpResponse(html)'''
    visitor_cookie_handler(request)
    context_dic["visits"] = request.session["visits"]
    return render(request, 'rango/index_base.html', context=context_dic)


def show_category(request, slug_category_name):
    context_dic = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=slug_category_name)
        # Retrieve all of the associated pages.
        # Note that filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)
        # Adds our results list to the template context under name pages.
        context_dic['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dic['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dic['category'] = None
        context_dic['pages'] = None

    return render(request, "rango/category_base.html", context_dic)

def about(request):
    context_dic = {
        "username": "Test_Rango_User",
    }

    visitor_cookie_handler(request)
    context_dic["visits"] = request.session["visits"]
    
    '''
    html='Rango says here is the about page. <br\> <a href="/rango/">Main Page</a>'
    return HttpResponse(html)'''
    return render(request, "rango/about_base.html", context=context_dic)


@login_required
def add_category(request):
    form = CategoryForm()

    # HTTP POST
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)


    return render(request, "rango/add_category_base.html", {'form': form})

@login_required
def add_page(request, slug_category_name):
    try:
        category = Category.objects.get(slug=slug_category_name)
    except DoesNotExist:
        category = None

    if not category:
        return index(request)

    form = PageForm()

    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, slug_category_name)
        else:
            print(form.errors)

    context_dict = {
        "form": form,
        "category": category
    }
    return render(request, "rango/add_page_base.html", context_dict)


def get_serve_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val

    return val 

def visitor_cookie_handler(request):
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(request.COOKIES.get('visits', '1'))
    # last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    # To get session detail from server side instead of storing in client side (request)
    last_visit_cookie = get_serve_side_cookie(request, "last_visit", str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).seconds > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    # Update/set the visits cookie
    request.session['visits'] = visits

'''
def register(request):
    registered = False
    user_form = UserForm()
    user_profile_form = UserProfileForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)

        if user_form.is_valid and user_profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = user_profile_form.save(commit=False)
            profile.user = user
            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]
            profile.save()

            registered = True
        else:
            print(user_form.errors, user_profile_form.errors)            
        
    context_dic = {
        "user_form": user_form,
        "user_profile_form": user_profile_form,
        "registered": registered
    }

    return render(request, "rango/register.html", context_dic)

def user_login(request):
    if request.method == "POST":
        # get username & password info & validate they are valid using authenticate method
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango Account is disabled")
        else:
            return HttpResponse("Invalid login details provided.")
    
    return render(request, 'rango/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


'''


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})
    #return HttpResponse("Since you are logged in, you can see the content!!")
