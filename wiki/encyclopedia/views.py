from django.shortcuts import render
from django import forms
from . import util
import markdown
from random import randint

#class ArticleSearchForm(forms.Form):


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def hello(request):
    return render(request, "encyclopedia/hello.html")

def article(request, article):
    entry = util.get_entry(article)
    markdowner = markdown.Markdown()
    if entry == None:
        return render(request, "encyclopedia/error.html", {
            "title": article
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "content": markdowner.convert(entry),
            "title": article
        })

def search(request):
    if request.method == "POST":
        query = request.POST['q']
        entries = util.list_entries()
        substrings = []
        for x in entries:
            if query.lower() == x.lower():
                entry = util.get_entry(query.capitalize())
                markdowner = markdown.Markdown()
                return render(request, "encyclopedia/entry.html", {
                    "content": markdowner.convert(entry),
                    "title": article
                })
            elif query.lower() in x.lower():
                substrings.append(x)
        return render(request, "encyclopedia/index.html", {
            "entries": substrings
        })
    
def new_page(request):
    if request.method=="POST":
        title = request.POST['title']
        content = request.POST['content']
        if title in util.list_entries():
            return render(request, "encyclopedia/newpageerror.html", {
                "title": title
            })
        else:
            util.save_entry(title, content)
            return article(request, title)
    else:
        return render(request, "encyclopedia/newpage.html")
    
def edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "content": content,
            "title": title
        })
    
def edit_save(request):
    if request.method=="POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return article(request, title)
    
def random(request):
    if request.method == "GET":
        entries = util.list_entries()
        x = randint(0, len(entries) - 1)
        title = entries[x]
        return article(request, title)

