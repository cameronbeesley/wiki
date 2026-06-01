from django import forms
from django.shortcuts import render
from django.shortcuts import redirect
import markdown2
from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def visit_entry(request, entry):
    contents = util.get_entry(entry)
    if contents is None:
        return render(request, "encyclopedia/page_not_found.html")
    else:
        return render(request, "encyclopedia/wiki.html", {
            "entry": entry,
            "contents": markdown2.markdown(contents)
        })
    
def searching(request):
    query = request.GET.get('q', '')

    if util.get_entry(query) is not None:
        return redirect('wiki', entry=query)
    else:
        return redirect('search', query=query)
    
def search(request, query):
    possible_searches = []
    for search in util.list_entries():
        if query.lower() in search.lower():
            possible_searches.append(search)
    if len(possible_searches) == 0:
        possible_searches = None
    return render(request, "encyclopedia/search_page.html", {
        "query": query,
        "entries": possible_searches
    })

class new_page_form(forms.Form):
    title = forms.CharField(
        label="Page Title",
        widget=forms.TextInput(attrs={
            "class": "title-area"
        }))
    content = forms.CharField(
        label="Page Content",
        widget=forms.Textarea(attrs={
            "class": "content-area"
        }))

def new_page(request):
    if request.method == "POST":
        form = new_page_form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title not in util.list_entries():
                util.save_entry(title, content)
                return redirect('index')
            else:
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "error_messages": ["Title already exists. Change title or got to edit page."]
                })
        else:
            return render(request, "encyclopedia/new_page.html", {
                "form": form,
                "error_messages": ["Information is invalid. Try again."]
            })

    return render(request, "encyclopedia/new_page.html", {
        "form": new_page_form(),
        "error_messages": []
    })

class edit_page_form(forms.Form):
    content = forms.CharField(
        label="Page Content",
        widget=forms.Textarea(attrs={
            "class": "content-area"
        }))
    
def edit(request, entry):
    if request.method == "POST":
        form = edit_page_form(request.POST)
        if form.is_valid():
            title = entry
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('index')
        else:
            return render(request, "encyclopedia/edit_page.html", {
                "entry": entry,
                "form": form,
                "error_messages": ["Information is invalid. Try again."]
            })

    return render(request, "encyclopedia/edit_page.html", {
        "entry": entry,
        "form": edit_page_form(initial={"content": util.get_entry(entry)}),
        "error_messages": []
    })

def random(request):
    entry = choice(util.list_entries())
    return redirect("wiki", entry=entry)