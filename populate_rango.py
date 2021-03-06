import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainsite.settings')
django.setup()

from rango.models import Category, Page

def populate():
    # create data for pages and its corresponding urls for each category
    python_pages = [
        {"title": "Official Python Tutorial", 
        "url":"http://docs.python.org/2/tutorial/",
        "views": 56},
        {"title":"How to Think like a Computer Scientist", 
        "url":"http://www.greenteapress.com/thinkpython/",
        "views": 50},
        {"title":"Learn Python in 10 Minutes", 
        "url": "https://docs.djangoproject.com/en/1.9/ref/contrib/admin/",
        "views": 23},
    ]
    django_pages = [
        {"title":"Official Django Tutorial", 
        "url":"https://docs.djangoproject.com/en/4.0/intro/tutorial01/",
        "views": 5},
        {"title":"Django Rocks", "url":"http://www.djangorocks.com/",
        "views": 6},
        {"title":"How to Tango with Django", "url":"http://www.tangowithdjango.com/",
        "views": 7}
    ]
    other_pages = [
        {"title":"Bottle", "url":"http://bottlepy.org/docs/dev/",
        "views": 2},
        {"title":"Flask", "url":"http://flask.pocoo.org", "views": 8}
    ]

    # map category with above pages
    cats = {
       "Python": {"pages": python_pages, "views": 128, "likes": 64},
       "Django": {"pages": django_pages, "views": 64, "likes": 32},
       "Other Frameworks": {"pages": other_pages, "views": 32, "likes": 16}
    }

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    c.save()
    return c

if __name__ == "__main__":
    print("start populating script for rango app.")
    populate()
