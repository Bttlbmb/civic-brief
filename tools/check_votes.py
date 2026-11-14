"""Compare the four published votes with the original workbook, offline.

Usage: python3 tools/check_votes.py /path/to/20261112_1.xlsx
The SHA-256 identifies the exact file reviewed for the November snapshot.
"""
import argparse
from hashlib import sha256
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from snapshot import PLACES, load

ORIGINAL = 'https://www.bundestag.de/resource/blob/1233020/20261112_1.xlsx'
FINGERPRINT = next(row['sha256'] for row in load('record-versions.json')['records'] if row['url'] == ORIGINAL)
OPTIONS = {'ja': 'Yes', 'nein': 'No', 'Enthaltung': 'Abstained',
           'ungültig': 'Invalid', 'nichtabgegeben': 'Did not vote'}


def verify(path):
    if sha256(path.read_bytes()).hexdigest() != FINGERPRINT:
        raise ValueError('Different workbook: check the official source and its checksum.')
    with ZipFile(path) as book:
        strings = [''.join(s.itertext()) for s in ET.fromstring(book.read('xl/sharedStrings.xml'))]
        sheet = ET.fromstring(book.read('xl/worksheets/sheet1.xml'))
    rows = {}
    for row in sheet.findall('.//{*}row'):
        cells = {}
        for cell in row.findall('{*}c'):
            value = cell.findtext('{*}v')
            if value is not None:
                column = cell.get('r').rstrip('0123456789')
                cells[column] = strings[int(value)] if cell.get('t') == 's' else value
        rows[int(row.get('r'))] = cells
    headers = rows[1]
    count = 0
    for place in PLACES.values():
        for level in place['levels']:
            for action in level.get('activities', []):
                if not any(ref['url'] == ORIGINAL for ref in action['sources']):
                    continue
                for vote in action.get('votes', []):
                    number = vote['source_row']
                    record = {headers[k]: v for k, v in rows[number].items()}
                    marked = [OPTIONS[k] for k in OPTIONS if record.get(k) == '1']
                    if (record['Bezeichnung'] != vote['name'] or marked != [vote['vote']]):
                        raise ValueError(f'Row {number}: name or vote does not match.')
                    print(f'{number:>3}  {record["Bezeichnung"]}: {marked[0]}')
                    count += 1
    if not count:
        raise ValueError('No published votes found for this roll call.')
    print(f'{count} published entries matched the original official workbook.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check the roll call against this snapshot.')
    parser.add_argument('xlsx', type=Path, help='Local copy of the Bundestag workbook 20261112_1.xlsx')
    try:
        verify(parser.parse_args().xlsx)
    except (OSError, KeyError, ValueError) as error:
        parser.exit(1, f'Check failed: {error}\n')
