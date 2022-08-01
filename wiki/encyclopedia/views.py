from turtle import title
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django import forms
import random
from django.contrib import messages

from . import util
from markdown2 import Markdown

import encyclopedia

markdowner = Markdown()

class WikiForm(forms.Form):
    name = forms.CharField(label="",max_length=100, widget=forms.TextInput(
        attrs={
            "placeholder": "Title",
            "class": "title-input",
        }
    ))
    text = forms.CharField(label="", max_length=1500, widget=forms.Textarea(
        attrs={
            "placeholder": "Content (markdown)",
            "class": "text-input"
        }
    ) )

class EditForm(forms.Form):
    text = forms.CharField(label="", max_length=1500, widget=forms.Textarea(
        attrs={
            "class": "text-input"
        }
    ))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entryPage = util.get_entry(title)
    if entryPage is None:
        return render(request, "encyclopedia/doesNotExist.html", {
            "title": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "body": markdowner.convert(entryPage)
    })

def new_entry(request):
    if request.method == "POST":
        form = WikiForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data["name"].title()
            text = form.cleaned_data["text"]
            entries = util.list_entries()
            if name in entries:
                messages.error(request, f'"{name}" already exists. Please choose another title.')
                return redirect('new_entry')
            else:
                util.save_entry(name, text)
                entry = util.get_entry(name)
                entry_convert = markdowner.convert(entry)

            return HttpResponseRedirect(f"wiki/{name}")
           
    else:
        form = WikiForm()
    return render(request, "encyclopedia/new_entry.html", {
        "form": form, 
    })


def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        context = {
            "form": EditForm(initial={"text": content}),
            "title": title
        }
        return render(request, "encyclopedia/edit.html", context)

    elif request.method == "POST":
        form = EditForm(request.POST)
        
        if form.is_valid():
            text = form.cleaned_data["text"].encode()
            entries = util.list_entries()
            util.save_entry(title, text)
            entry = util.get_entry(title)
            entry_convert = markdowner.convert(entry)

            return HttpResponseRedirect(f"/wiki/{title}")

def random_page(request):
    page = util.list_entries()
    rand_page = random.choice(page)
    return HttpResponseRedirect(f"/wiki/{rand_page}")


def search(request):
    entry_search = request.POST["q"]
    entries = util.list_entries()
    match = [entry for entry in entries if entry_search.lower() == entry.lower()]
    partial = [entry for entry in entries if entry_search.lower() in entry.lower()]

    if len(match) > 0 :
        return HttpResponseRedirect(f"/wiki/{entry_search}")

    return render(request, "encyclopedia/search.html", {
        "partial": partial,
        "title": "Search Results",
        "entry": entry_search
    })