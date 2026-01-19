import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

# static
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(PROJECT_DIR, "static")),
    name="static"
)

# snapshots
app.mount(
    "/snapshots",
    StaticFiles(directory=os.path.join(PROJECT_DIR, "snapshots")),
    name="snapshots"
)

templates = Environment(
    loader=FileSystemLoader(os.path.join(PROJECT_DIR, "templates"))
)
