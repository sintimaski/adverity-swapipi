import json
import datetime

import requests

from .consts import SWAPI_URL, FIELDS_TO_EXCLUDE_PEOPLE
from django.http import Http404


def _get_all_entries(resource: str):
    query = _get_url_for_resource(resource)
    entries = []
    has_next = True
    try:
        while has_next:
            response = requests.get(query)
            json_data = json.loads(response.content)
            entries.extend(json_data["results"])
            if bool(json_data["next"]):
                query = json_data["next"]
            else:
                has_next = False
    except requests.exceptions.Timeout:
        # As an example for exceptions catching.
        # For more convenient usage better to create separate class for requests with
        # all needed exceptions and infrastructure. Also, DRF would solve problem
        # with rising exceptions.
        raise Http404
    return entries


def _get_url_for_resource(resource: str):
    return f"{SWAPI_URL}/{resource}"


def _transform_people(people: list, planets: dict):
    for person in people:
        person["homeworld"] = planets.get(person["homeworld"], {}).get("name", "")
        # Would be faster than converting to datetime -> formatting -> to str.
        person["date"] = person["edited"].split("T")[0]
        for field in FIELDS_TO_EXCLUDE_PEOPLE:
            person.pop(field, None)


def _get_new_file_name_path():
    pass
