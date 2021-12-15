from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context_dic = {
        'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"
    }
    '''html='Rango says hey there partner! <br\> <a href="/rango/about/">About</a>'
    return HttpResponse(html)'''
    return render(request, 'rango/index.html', context=context_dic)

def about(request):
    context_dic = {
        "username": "Test_Rango_User",
    }
    '''
    html='Rango says here is the about page. <br\> <a href="/rango/">Main Page</a>'
    return HttpResponse(html)'''
    return render(request, "rango/about.html", context=context_dic)