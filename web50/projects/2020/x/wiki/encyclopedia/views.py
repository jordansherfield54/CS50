from django.shortcuts import render
import markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, entry):
    result = util.get_entry(entry)
    if result:
        result = markdown2.markdown(result)
        return render(request, "encyclopedia/entry.html", {
            "entry":result
        })
    else:
        return render(request, "encyclopedia/error.html")

