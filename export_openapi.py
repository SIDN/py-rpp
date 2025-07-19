from rpp.main import app
import json
import sys

json.dump(app.openapi(), sys.stdout, indent=2)