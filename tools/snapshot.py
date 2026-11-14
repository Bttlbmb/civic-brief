"""The site reads only its compiled HTML, never these editorial input files."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'docs'

def load(name):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))

SNAPSHOT = load('snapshot.json')
PLACES = SNAPSHOT['places']
AREAS = load('city-districts.json')
