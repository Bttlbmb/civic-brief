"""Compile the reviewed snapshot into portable HTML. No network or dependencies."""
from datetime import date
from html import escape as h
from areas import area_block
from events import event_bytes
from icons import icon, logo
from snapshot import OUTPUT, PLACES, SNAPSHOT

MONTHS = ('', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December')

def display_date(iso):
    day = date.fromisoformat(iso)
    return f'{day.day} {MONTHS[day.month]} {day.year}'

def story_date(iso):
    day = date.fromisoformat(iso)
    return f'{day.day} {MONTHS[day.month][:3]} {day.year}'

def home(city):
    return 'index.html' if city == 'bobingen' else city + '.html'

def representation(city):
    return city + '-representatives.html'

def source(ref, decorated=False):
    url, label = h(ref['url'], quote=True), h(ref['label'])
    language = h(ref.get('language', 'de'), quote=True)
    if decorated:
        return f'<a class="source" hreflang="{language}" href="{url}">{icon("doc")}{label}{icon("out")}</a>'
    return f'<a hreflang="{language}" href="{url}">{label}</a>'

def page(title, city, body, finder=False):
    name = h(PLACES[city]['name'])
    script = '<script defer src="assets/district.js"></script>' if finder else ''
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="Local news and elected representatives for Bobingen and Augsburg. Every update links to its source.">
  <title>{h(title)} · Civic Brief</title>
  <link rel="icon" href="assets/mark.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/style.css">
  {script}
</head>
<body>
  <a class="skip" href="#content">Skip to content</a>
  <header><div class="wrap bar">
    <a class="brand" href="{home(city)}" aria-label="Civic Brief – {name} overview">{logo}Civic Brief</a>
    <span class="edition">Local politics</span>
  </div></header>
  <main class="wrap" id="content" tabindex="-1">{body}</main>
  <footer class="wrap foot">
    <span>Civic Brief · Independent prototype</span>
    <a href="sources-{city}.html">Sources and coverage</a>
  </footer>
</body>
</html>
'''

def mast(city, detail=False):
    name = h(PLACES[city]['name'])
    title = 'Representatives in ' + name if detail else name
    route = representation if detail else home
    jump = '' if detail else (
        f'<a class="mobilejump" href="{representation(city)}">Who represents me? {icon("arr")}</a>')
    return f'''
      <div class="mast {'detail' if detail else ''}">
        <div class="mapbox" style="background-image:url(assets/{city}.svg)" aria-hidden="true"></div>
        <a class="mapcaption" href="sources-{city}.html#map">© BKG 2026 · Map credits</a>
        <div class="mastbody">
          <div class="kicker">{icon("pin")} Local edition · Swabia</div>
          <h1>{title}</h1><p>{h(PLACES[city]["place_type"])}</p>
        </div>
      </div>
      <div class="control">
        {place_switch(city, route)}
        <span class="stamp">As of {display_date(SNAPSHOT["as_of"])}</span>{jump}
      </div>'''

def place_switch(city, route):
    choices = []
    for key, place in PLACES.items():
        current = ' aria-current="page"' if city == key else ''
        choices.append(f'<a href="{route(key)}"{current}>{h(place["name"])}</a>')
    return ('<nav class="row" aria-label="Switch city"><span class="switchlabel">Your city</span>'
            + '<div class="switch">' + ''.join(choices) + '</div></nav>')

def sidebar(city):
    rows = []
    for level in PLACES[city]['levels']:
        key = level['id']
        rows.append(f'''
          <a class="navlink" href="{representation(city)}#{key}">
            <span class="ib">{icon(key)}</span><span><b>{h(level["level"])}</b>
            <small>{h(level["institution"])}</small></span>{icon("arr")}
          </a>''')
    return f'''<aside class="side" aria-label="Your representatives">
        <div class="sidehead"><div class="kicker">{icon("users")} Your representatives</div>
          <h2>Who represents me?</h2><p>Choose a level to see who represents you and how they are connected to your city.</p>
        </div>{''.join(rows)}
      </aside>'''

def cards(city):
    result = []
    for i, item in enumerate(PLACES[city]['updates']):
        pending = item['id'] in ('solar-panels', 'city-consultation')
        art = f'<img class="art" src="assets/{city}-story.svg" alt="">' if i == 0 else ''
        result.append(f'''
          <article class="card {'lead' if i == 0 else ''}">{art}<div class="words">
            <div class="eyeline">
              <span class="tag {'gold' if pending else ''}">{icon("clock" if pending else "check")}{h(item["status"])}</span>
              <time datetime="{h(item["date"])}">Published: {story_date(item["date"])}</time>
            </div>
            <h3><a class="storylink" href="sources-{city}.html#{h(item["id"])}">{h(item["title"])}</a></h3>
            <p>{h(item["text"])}</p>
            {source(item["source"], decorated=True)}
          </div></article>''')
    return ''.join(result)

def activities(level):
    blocks = []
    for entry in level.get('activities', []):
        state = ''
        if entry.get('date'):
            date_label = h(entry.get('date_label', 'Recorded'))
            state = (f'<p class="activity-state"><span class="tag gold">{h(entry["status"])}</span> '
                     f'<time datetime="{h(entry["date"])}">{date_label} {story_date(entry["date"])}</time></p>')
        local = ('<p class="local-context">' + h(entry['local_context']) + '</p>'
                 if entry.get('local_context') else '')
        evidence = ('<ul class="activity-links" aria-label="Sources">'
                    + ''.join('<li>' + source(ref) + '</li>' for ref in entry['sources'])
                    + '</ul>')
        votes = ''
        if 'votes' in entry:
            rows = ''.join(f'<tr><th scope="row">{h(v["name"])}</th><td>{h(v["vote"])}</td></tr>'
                           for v in entry['votes'])
            caption = h(entry.get('vote_caption', 'How they voted'))
            votes = (f'<table class="votes"><caption>{caption}</caption>'
                     '<thead><tr><th scope="col">Member</th><th scope="col">Vote</th></tr></thead>'
                     f'<tbody>{rows}</tbody></table>')
        blocks.append(f'''
          <div class="activity">{state}<h3>{h(entry["title"])}</h3>
            <p>{h(entry["text"])}</p>{local}{votes}{evidence}
          </div>''')
    return ''.join(blocks)

def details(city):
    blocks = []
    other = 'augsburg' if city == 'bobingen' else 'bobingen'
    compare_labels = {
        'city': 'city government', 'region': 'regional representatives',
        'state': 'state representatives', 'federal': 'federal representatives',
        'europe': 'European representation',
    }
    for level in PLACES[city]['levels']:
        key = level['id']
        if level.get('members'):
            heading = ' <span class="and">and</span> '.join(
                f'<span class="named-member">{h(member["name"])} '
                f'<span class="party">({h(member["party"])})</span></span>'
                for member in level['members'])
        else:
            heading = h(level['representatives'])
        links = ''.join('<li>' + source(r) + '</li>' for r in level['sources'])
        local_note = '<p>' + h(level['more_context']) + '</p>' if level.get('more_context') else ''
        scope = ''
        if level.get('scope'):
            scope = (f'<p class="representation-scope">{h(level["scope"])}</p>'
                     f'<p class="profile-label">{h(level["profile_label"])}</p>')
        extra = ''
        if city == 'augsburg' and key == 'state':
            extra = area_block()
        if city == 'augsburg' and key == 'region':
            extra = '<p><a href="#constituency">Find your city district</a></p>'
        target = 'city' if key == 'district' else key
        label = ('How Augsburg handles district duties' if key == 'district' else
                 f'See {PLACES[other]["name"]}’s {compare_labels[key]}')
        compare = (f'<p class="compare"><a href="{representation(other)}#{target}">'
                   + h(label) + ' ' + icon('arr') + '</a></p>')
        blocks.append(f'''
          <section class="profile" id="{key}" tabindex="-1" aria-labelledby="{key}-level {key}-name">
            <p class="kicker" id="{key}-level">{icon(key)} {h(level["level"])} · {h(level["institution"])}</p>
            {scope}<h2 id="{key}-name">{heading}</h2><p>{h(level["connection"])}</p>{local_note}
            {extra}{activities(level)}
            <p class="profile-sources-label">Profiles and records</p>
            <ul class="profile-links">{links}</ul>{compare}
            <p class="mobile-level-return"><a href="#levels-menu">Choose another level</a></p>
          </section>''')
    return ''.join(blocks)

def level_menu(city):
    labels = ''.join(f'<a href="#{r["id"]}">{icon(r["id"])}{h(r["level"])}</a>'
                     for r in PLACES[city]['levels'])
    return f'''<details class="levelmenu"><summary>Choose a level of government</summary>
      <nav id="levels-menu" tabindex="-1" aria-label="Levels of government">{labels}</nav></details>'''

def back(city):
    return f'<a class="back" href="{home(city)}">{icon("back")} Back to {h(PLACES[city]["name"])}</a>'

def notes(city):
    evidence = []
    for item in PLACES[city]['updates']:
        profile = item['level_id']
        level = next(r for r in PLACES[city]['levels'] if r['id'] == profile)
        follow_up = source(item['follow_up']) if item.get('follow_up') else ''
        if 'calendar' in item:
            follow_up += (f'<a href="calendar/{h(item["calendar"]["file"])}" download>'
                          'Save the meeting to your calendar (.ics)</a>')
        evidence.append(f'''
          <article class="evidence" id="{h(item["id"])}" tabindex="-1" aria-labelledby="{h(item["id"])}-title">
            <h3 id="{h(item["id"])}-title">{h(item["title"])}</h3>
            <p class="evidencedate">Published: {display_date(item["date"])} · {h(item["status"])}</p>
            <p>{h(item["evidence"])}</p>
            <div class="evidencelinks">{source(item["source"], decorated=True)}
              <a href="{representation(city)}#{profile}">Your representatives: {h(level["level"])}</a>{follow_up}</div>
          </article>''')
    switch = place_switch(city, lambda key: 'sources-' + key + '.html')
    return f'''<div class="notes">{back(city)}<h1>Sources and coverage</h1>
      <div class="notesswitch">{switch}</div>
      <p>As of {display_date(SNAPSHOT["as_of"])}. Civic Brief is an independent prototype.
        We write in English. Most original records are in German; we link to official English versions where available.</p>
      <h2>Behind the stories in {h(PLACES[city]["name"])}</h2>{''.join(evidence)}
      <h2>How do we choose stories?</h2>
      <p>We select a few local developments and put the most recent notice first.
        On the overviews, dates tell you when the source published its update.
        Meeting and decision dates appear in the text. Parliamentary votes use the date of the vote.</p>
      <h2>What counts as a decision?</h2>
      <p>An agenda tells you what a committee plans to discuss. It does not tell you what the committee decided.
        We report an individual vote only when the minutes or a roll call name the voter.</p>
      <h2>Which representatives appear here?</h2>
      <p>We include directly elected officials and a selection of members elected from party lists.
        Each profile explains the person’s connection to the city. The linked directories cover more members.</p>
      <h2>How current is this?</h2>
      <p>This is a dated snapshot. It changes only when the records are checked again.
        Follow the source links for later developments.</p>
      <h2 id="map" tabindex="-1">About the map</h2>
      <p>The map shows municipal boundaries, not electoral districts.
        Map data © <a href="https://www.bkg.bund.de">BKG</a> 2026,
        <a href="https://www.govdata.de/dl-de/by-2-0">dl-de/by-2-0</a>.
        We cropped, simplified and labelled the VG250 municipal boundaries dated 1 January 2025.
        <a href="https://sgx.geodatenzentrum.de/web_public/gdz/datenquellen/datenquellen_vg_nuts.pdf">BKG data sources (PDF)</a>.</p></div>'''

def render():
    for city, place in PLACES.items():
        name = place['name']
        for story in place['updates']:
            if 'calendar' in story:
                event = story['calendar']
                (OUTPUT / 'calendar').mkdir(exist_ok=True)
                (OUTPUT / 'calendar' / event['file']).write_bytes(
                    event_bytes(event, story['source']['url'], SNAPSHOT['as_of']))
        overview = mast(city) + f'''
          <div class="columns">
            <section aria-labelledby="news">
              <div class="sectionhead">{icon("paper")}<h2 id="news">What just happened?</h2></div>
              {cards(city)}
            </section>{sidebar(city)}
          </div>'''
        who = mast(city, detail=True) + back(city) + level_menu(city) + f'''
          <div class="detailgrid"><div>{details(city)}</div>{sidebar(city)}</div>'''
        pages = {
            home(city): page('Local updates: ' + name, city, overview),
            representation(city): page('Who represents me in ' + name + '?', city, who, finder=city == 'augsburg'),
            'sources-' + city + '.html': page('Sources and coverage: ' + name, city, notes(city)),
        }
        for filename, html in pages.items():
            (OUTPUT / filename).write_text(html, encoding='utf-8')
    (OUTPUT / 'assets/mark.svg').write_text(
        logo.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"')
            .replace('stroke="#c8d8b8"', 'fill="#154b39"'), encoding='utf-8')
    (OUTPUT / '.nojekyll').touch()

if __name__ == '__main__':
    render()
