from os.path import dirname, join

FILES_PATH = join(dirname(__file__), "files")
SWAPI_URL = "https://swapi.dev/api"
FIELDS_TO_EXCLUDE_PEOPLE = [
    "films",
    "species",
    "vehicles",
    "starships",
    "created",
    "edited",
    "url",
]
