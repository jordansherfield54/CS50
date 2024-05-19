from django.shortcuts import render
import markdown2
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random


class NewEntry(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':4}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, entry):
    result = util.get_entry(entry)
    if result:
        result = markdown2.markdown(result)
        return render(request, "encyclopedia/entry.html", {
            "title": entry,
            "entry": result
        })
    else:
        return render(request, "encyclopedia/error.html", {
                    "errors": ["404: Sorry this page doesn't Exist"]
                })

def partial(lst, query):
    return [s for s in lst if query.lower() in s.lower()]

def search(request):
    search_query = request.GET.get('q',"")
    list_entries = util.list_entries()
    for i in list_entries:
        if search_query.lower() == i.lower():
            result = util.get_entry(i)
            if result:
                result = markdown2.markdown(result)
                return render(request, "encyclopedia/entry.html", {
                    "title": i,
                    "entry": result
                })

    matches = partial(list_entries, search_query)
    return render(request, "encyclopedia/index.html", {
    "entries": matches
    })


def add(request):
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if not util.get_entry(title):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:index"))
            else:
                return render(request, "encyclopedia/error.html", {
                    "errors": ["An Entry with this title already Exists please edit the existing one"]
                })

        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })


    return render(request, "encyclopedia/add.html", {
        "form": NewEntry()
    },)

def save_after_edit(request):
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                util.save_entry(title, content)
                # return HttpResponseRedirect(reverse("encyclopedia:index"))
                return HttpResponseRedirect(reverse("encyclopedia:page", args=[title]))
            else:
                return render(request, "encyclopedia/error.html", {
                    "errors": ["You are trying to edit an entry that does not exist"]
                })

        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })

def edit(request, title):
    # title = request.GET.get(title)
    

    form = {
        "title" : title,
        "content" : util.get_entry(title)
    }
    form = NewEntry(form)
    return render(request, "encyclopedia/edit.html", {
        "form": form
    },)
    
        
def random_page(request):
    entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("encyclopedia:page", args=[entry]))

    