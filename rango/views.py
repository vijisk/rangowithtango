from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category, Page

def index(request):
    # Display top level liked 5 categories in main page
    # get list of 5 categories by order 
    category_list = Category.objects.order_by("-likes")[:5]
    page_list = Page.objects.order_by("-views")[:5]
    context_dic = {
        "categories": category_list,
        "pages": page_list
    }
    '''
    context_dic = {
        'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"
    }
    html='Rango says hey there partner! <br\> <a href="/rango/about/">About</a>'
    return HttpResponse(html)'''
    return render(request, 'rango/index.html', context=context_dic)

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

    return render(request, "rango/category.html", context_dic)

def about(request):
    context_dic = {
        "username": "Test_Rango_User",
    }
    '''
    html='Rango says here is the about page. <br\> <a href="/rango/">Main Page</a>'
    return HttpResponse(html)'''
    return render(request, "rango/about.html", context=context_dic)