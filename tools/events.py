"""Build small, portable calendar files from a meeting's official details."""
from datetime import date, datetime, timezone


def escape_value(value):
    return (value.replace('\\', '\\\\').replace('\r\n', '\n').replace('\r', '\n')
            .replace('\n', '\\n').replace(';', '\\;').replace(',', '\\,'))


def fold_line(value):
    """RFC 5545 uses 75 UTF-8 bytes per physical line, not 75 characters."""
    out, line, length = [], [], 0
    for char in value:
        size = len(char.encode('utf-8'))
        if length + size > 75:
            out.append(''.join(line))
            line, length = [' '], 1
        line.append(char)
        length += size
    return out + [''.join(line)]


def event_bytes(event, source, as_of):
    start = datetime.fromisoformat(event['start_local'])
    if start.tzinfo is None:
        raise ValueError('A calendar item must include its local time offset.')
    lines = [
        'BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Civic Brief//Public meetings//EN',
        'CALSCALE:GREGORIAN', 'BEGIN:VEVENT',
        'UID:' + event['file'].removesuffix('.ics') + '@civic-brief.invalid',
        'DTSTAMP:' + date.fromisoformat(as_of).strftime('%Y%m%d') + 'T000000Z',
        'DTSTART:' + start.astimezone(timezone.utc).strftime('%Y%m%dT%H%M%SZ'),
        'SUMMARY:' + escape_value(event['summary']),
        'LOCATION:' + escape_value(event['location']),
        'DESCRIPTION:' + escape_value(event['description']),
        'URL:' + source, 'END:VEVENT', 'END:VCALENDAR',
    ]
    return ('\r\n'.join(part for line in lines for part in fold_line(line)) + '\r\n').encode('utf-8')
