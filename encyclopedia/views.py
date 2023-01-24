from django.shortcuts import render
from django import forms
import random
from markdown2 import markdown
from . import util


# form to edit old pages/entries
class editForm(forms.Form):
    title = forms.CharField(label="Title", required=True)
    body = forms.CharField(label="Body", required=True, widget=forms.Textarea())


# Searchbar
class searchForm(forms.Form):
    search = forms.CharField(required=True)


# form To make new pages/enteries
class ADDpageForm(forms.Form):
    title = forms.CharField(label="Enter Title", required=True)
    body = forms.CharField(label="Enter Body", required=True, widget=forms.Textarea())


searchbar = searchForm()
newpage = ADDpageForm()
editpage = editForm()


# index
def index(request):
    return render(
        request,
        "encyclopedia/index.html",
        {"entries": util.list_entries(), "form": searchbar},
    )


# to view selected page or page entered in url
def entry(request, entry):
    page = util.get_entry(entry)
    if page is None:
        return render(
            request, "encyclopedia/page is not available.html", {"form": searchbar}
        )
    else:
        Body = markdown(page)
        return render(
            request,
            "encyclopedia/entry.html",
            {"title": entry, "Body": Body, "form": searchbar},
        )


# search function
def search(request):
    searchbar = searchForm(request.POST)
    searchbar.is_valid()
    data = searchbar.cleaned_data.get("search")
    Page = False
    for entry in util.list_entries():
        if data.upper() == entry.upper():
            Entry = util.get_entry(data)
            Body = markdown(Entry)
            Page = True
            break
    # if page/entry found load encyclopedia/entry.html
    if Page:
        return render(
            request,
            "encyclopedia/entry.html",
            {"Body": Body, "form": searchbar, "title": data},
        )
        # checking substring
        # MS = matching substring
    else:
        MS = []
        for entry in util.list_entries():
            if data.upper() in entry.upper():
                MS.append(entry)

        # list of entries with substring on index
        if len(MS) != 0:
            return render(
                request,
                "encyclopedia/index.html",
                {"entries": MS, "form": searchbar},
            )

        # if no match load page is not available template
        else:
            return render(
                request,
                "encyclopedia/page is not available.html",
                {"form": searchbar},
            )


# view to create new pages/entries
def Newpage(request):
    # if accesed using POST
    if request.method == "POST":
        newpage = ADDpageForm(request.POST)
        if newpage.is_valid():
            # getting title and body data
            title = newpage.cleaned_data["title"]
            body = newpage.cleaned_data["body"]
            present = False
            for entry in util.list_entries():
                if title == entry:
                    present = True
                    break
            if present:
                return render(
                    request,
                    "encyclopedia/page already exists.html",
                    {"form": searchbar},
                )
            else:
                util.save_entry(title, body)
                page = util.get_entry(title)
                Body = markdown(page)
                return render(
                    request,
                    "encyclopedia/entry.html",
                    {"title": title, "Body": Body, "form": searchbar},
                )
    # if accesed using GET
    else:
        newpage = ADDpageForm()
        return render(
            request,
            "encyclopedia/Newpage.html",
            {"form": searchbar, "newpage": newpage},
        )


# Edit selected page/entry
def edit(request, entry):
    if request.method == "POST":
        editpage = editForm(request.POST)
        if editpage.is_valid():
            entry = editpage.cleaned_data["title"]
            body = editpage.cleaned_data["body"]
            # saving Body using save_entry funcyion in util.py
            util.save_entry(entry, body)
            Body = markdown(body)
            return render(
                request,
                "encyclopedia/entry.html",
                {"title": entry, "Body": Body, "form": searchbar},
            )
    else:
        editpage = editForm({"title": entry, "body": util.get_entry(entry)})
        return render(
            request, "encyclopedia/edit.html", {"form": searchbar, "editform": editpage}
        )


# random page button
def rand(request):
    entrieslist = util.list_entries()
    Length = len(entrieslist)
    # genetrating random index number to choose a random fie from a list of entries
    Index = random.randint(0, Length - 1)
    title = entrieslist[Index]
    page = util.get_entry(title)
    Body = markdown(page)
    return render(
        request,
        "encyclopedia/rand.html",
        {"form": searchbar, "title": title, "Body": Body},
    )
