from collections import OrderedDict
from os.path import join, exists
from uuid import uuid4

import petl
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from .consts import FILES_PATH
from .helpers import _get_all_entries, _transform_people
from .models import FileMeta


def index(request):
    # Assuming that amount of files would be reasonable, no pagination requested
    files = FileMeta.objects.order_by("-created_at").all()
    return render(request, "index.html", {"entries": files})


def dataset(request, uid):
    limit = int(request.GET.get("limit", 10))
    filepath = join(FILES_PATH, f"{uid}.csv")
    if not exists(filepath):
        raise Http404

    people_table = petl.fromcsv(filepath)
    headers = people_table[0]

    limit = min(len(people_table), limit)
    people = people_table[1:limit]

    return render(
        request,
        "dataset.html",
        {"entries": people, "headers": headers, "limit": limit},
    )


def value_count(request, uid):
    fields = request.GET.get("fields", "").split(",")

    filepath = join(FILES_PATH, f"{uid}.csv")
    if not exists(filepath):
        raise Http404

    people_table = petl.fromcsv(filepath)
    headers = people_table[0]

    fields = [x for x in fields if x in headers]

    # Using internal powers of petl for grouping.
    if len(fields) > 0:
        people = petl.aggregate(
            people_table,
            key=tuple(fields),
            aggregation=len,
        )
        people = people[1:]
    else:
        people = list(people_table[1:])

    return render(
        request,
        "value_count.html",
        {"entries": people, "headers": headers, "fields": fields},
    )


def collect_entries(request):
    # For the larger amounts of data processed in variables, it is better to delete them
    # after usage (planets_list). Won't be an issue if stored in DB.
    # In that specific case would be even better to transform planets on-fly, while
    # fetching, creating list of dictionaries like [{url: name}].
    planets_list = _get_all_entries("planets")
    planets_url_to_name = dict(
        (lambda x: (x["url"], planet))(planet) for planet in planets_list
    )

    people = _get_all_entries("people")
    _transform_people(people, planets_url_to_name)

    uid = str(uuid4())
    filename = f"{uid}.csv"
    filepath = join(FILES_PATH, filename)

    people_table = petl.fromdicts(people)
    petl.tocsv(people_table, filepath)

    meta = FileMeta(name=uid)
    meta.save()

    return redirect("/")
