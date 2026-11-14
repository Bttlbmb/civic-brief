"""Compile one source of district mappings into both sides of the optional finder."""
from html import escape
from snapshot import AREAS

def area_block():
    districts = AREAS['districts']
    seats = AREAS['constituencies']
    options = []
    for district in sorted(districts, key=lambda d: d['name'].casefold()):
        number = escape(district['number'])
        area = escape(district['constituency'])
        name = escape(district['name'])
        options.append(f'<option value="{number}" data-half="{area}">{name} ({number})</option>')

    sections = []
    for area, seat in seats.items():
        sections.append(f'''
          <section data-result="{escape(area)}" id="members-{escape(area)}" tabindex="-1">
            <h4>{escape(seat["name"])} ({int(seat["number"])})</h4>
            <p class="mandates"><span>Bavarian Parliament: {escape(seat["state_member"])}</span>
              <span>Swabian Regional Assembly: {escape(seat["regional_member"])}</span></p>
          </section>''')
    rows = []
    for district in sorted(districts, key=lambda d: d['number']):
        number, name, area = (escape(district[k]) for k in ('number','name','constituency'))
        direction = area.title()
        rows.append(f'<tr><th scope="row"><span>{number}</span> {name}</th>'
                    f'<td><a href="#members-{area}" aria-label="{direction} representatives for {name}">'
                    f'{direction}</a></td></tr>')
    return f'''
      <div class="finder" id="constituency" tabindex="-1">
        <h3>Who represents my part of Augsburg?</h3>
        <p>The Bavarian Parliament and the Swabian Regional Assembly use the same two constituencies here.
          Federal elections use different boundaries.</p>
        <div id="district-controls" hidden>
          <label for="district-choice">Your city district</label>
          <select id="district-choice">
            <option value="">Choose your city district</option>
            {''.join(options)}
          </select>
          <div role="status" id="district-answer" aria-live="polite" aria-atomic="true"></div>
        </div>
        <details class="district-reference"><summary>Browse all 42 city districts</summary>
          <p>Find your district number, then follow East or West to the elected members.</p>
          <table class="district-table"><caption>City districts in number order</caption>
            <thead><tr><th scope="col">City district</th><th scope="col">Seat</th></tr></thead>
            <tbody>{''.join(rows)}</tbody></table>
          {''.join(sections)}
        </details>
        <p class="address-help">Unsure of your district?
          Find your street and house number in the <a href="{escape(AREAS["street_directory"])}#page=11">city street directory (PDF, in German)</a>.
          The “Stadtbezirk” column gives the district number to look up here.</p>
      </div>'''
