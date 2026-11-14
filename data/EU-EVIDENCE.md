# EU development and named-vote evidence

Checked on 14 November 2026 UTC for the prototype's snapshot. This note records the public official sources used for the EU addition and the exact scope of individual vote attribution.

## Development and procedural status

The European Parliament's Legislative Observatory records a decision on 12 November 2026 on procedure `2025/0223(COD)`, covering the Union Civil Protection Mechanism and Union support for health emergency preparedness and response. Its events table also records referral back to the committee for interinstitutional negotiations on that date. The text is a partial first-reading vote. Final EU rules and funding still require agreement.

[Official procedure file and chronology](https://oeil.europarl.europa.eu/oeil/en/procedure-file?reference=2025/0223(COD))

The status at the top of the procedure file still says it is awaiting Parliament's first-reading position. This is consistent with amendments being adopted and the file being sent back for negotiations before the formal first-reading position is concluded. Use “Negotiating position” in the interface. Do not call this final enactment or an award of local funding.

The official record names joint rapporteurs Leire Pajín and Aurelijus Veryga. An associated press release and EPRS summary describe the negotiating mandate, but Parliament's press-room HTML, PDF and named-vote XML returned JavaScript verification or empty responses in this review. The evidence below comes directly from the accessible official Open Data API and Legislative Observatory.

## Single official ballot

The documented `GET /events/{event-id}` endpoint returns the single ballot as JSON-LD. It is approximately 15 KB and is a narrower reader link than the full sitting's results.

[Official ballot JSON](https://data.europarl.europa.eu/api/v2/events/MTG-PL-2026-11-12-DEC-200101?format=application%2Fld%2Bjson)

[Official API documentation](https://data.europarl.europa.eu/en/developer-corner/opendata-api)

| Field | Value observed |
| --- | --- |
| `activity_id` | `MTG-PL-2026-11-12-DEC-200101` |
| `activity_date` | `2026-11-12` |
| `activity_start_date` | `2026-11-12T11:27:08+01:00` |
| `activity_order` | `64.0` |
| `activity_label.en` | `A10-0271/2026 – Leire Pajín, Aurelijus Veryga – Commission proposal` |
| `headingLabel.en` | `Draft legislative act` |
| `referenceText.en` | `Commission proposal` |
| `decision_method` | `def/ep-decision-methods/VOTE_ELECTRONIC_ROLLCALL` |
| `decision_outcome` | `def/ep-statuses/ADOPTED` |
| `number_of_votes_favor` | `424` |
| `number_of_votes_against` | `105` |
| `number_of_votes_abstention` | `83` |
| `number_of_attendees` | `612` |
| `recorded_in_a_realization_of` | `eli/dl/doc/PV-10-2026-11-12-RCV-ITM-019` |

`had_voter_favor` contains `person/1917`. Neither `had_voter_against` nor `had_voter_abstention` contains that identifier. Their list sizes also match the official aggregate counts.

## Named identity

The single ballot uses person identifiers. The documented `GET /meps/{mep-id}` endpoint identifies this voter.

[Official Markus Ferber person record](https://data.europarl.europa.eu/api/v2/meps/1917?format=application%2Fld%2Bjson)

| Field | Value observed |
| --- | --- |
| `id` | `person/1917` |
| `identifier` | `1917` |
| `label` | `Markus FERBER` |
| `familyName` | `Ferber` |
| `givenName` | `Markus` |

The full sitting endpoint with `json-layout=framed-and-included` independently returns the same ballot and an included person object with full ID `https://data.europarl.europa.eu/person/1917`, the same name fields, country `DE` and political group `PPE`. Adding that layout parameter to the single-event endpoint did not include names in its response. For a compact offline evidence bundle, retain the single ballot and person response together.

[Official sitting decisions with included named people](https://data.europarl.europa.eu/api/v2/meetings/MTG-PL-2026-11-12/decisions?vote-method=ROLL_CALL_EV&format=application%2Fld%2Bjson&json-layout=framed-and-included&offset=0&limit=1000)

## Corrections and intentions

All keys in the single ballot were inspected. The only intention field present is `had_voter_intended_abstention`, containing `person/257050`. Ferber's identifier `person/1917` is absent. No intended-favour, intended-against or other Ferber correction field appears in this ballot response. The full sitting response has the same result for this ballot.

The safe reported result for Ferber is his recorded **Yes** on this ballot. The review establishes the official data available when retrieved, with later official corrections remaining possible.

## Exact ballot scope and separate referral

The official vote-results record for item `MTG-PL-2026-11-12-VOT-ITM-993371` groups amendment decisions and this draft-act ballot together. The electronic ballot is order 64 in that item, following the amendment votes. “Vote on the amended proposal” is a concise description of its place in that sequence. “Vote on the draft legislative act” follows the official heading most literally.

[Official sitting vote-results record](https://data.europarl.europa.eu/api/v2/meetings/MTG-PL-2026-11-12/vote-results?format=application%2Fld%2Bjson&offset=0&limit=1000)

The request for referral back to committee is a separate decision, `MTG-PL-2026-11-12-DEC-200102`, order `65.0`. Its `referenceText.en` is `Request for referral back to committee`, its method is `def/ep-decision-methods/VOTE_HAND` and its outcome is `ADOPTED`. The record contains no named individual votes. Attribute the referral to Parliament as a body. Ferber's named Yes on decision 200101 does not establish how he voted on decision 200102.

[Official separate referral decision](https://data.europarl.europa.eu/api/v2/events/MTG-PL-2026-11-12-DEC-200102?format=application%2Fld%2Bjson)

## Local relevance

Bobingen's local context is supported by the Bavarian water authority's report, printed page 17. It states that the Holzhausen flood-retention basin helped protect Bobingen and other downstream towns in the June 2024 floods.

[Donauwörth water authority flood report, page 17](https://www.wwa-don.bayern.de/themen/hochwasser/hochwasserereignisse/doc/hochwasserbericht_2024.pdf#page=17)

Augsburg's own press release of 5 June 2024 reports 356 fire-service deployments in the city since Saturday 1 June. This is an independent-city source and does not rely on Landkreis Augsburg's disaster declaration.

[City of Augsburg flood-response account](https://www.augsburg.de/aktuelles-aus-der-stadt/detail/hochwasserschutz-in-augsburg)

These local records establish that flood preparation matters in the selected places. They do not establish that any project receives funding from this proposed EU programme.

## Retrieval fingerprints

The following are SHA-256 hashes of original raw response bytes retrieved during this review. JSON key ordering may differ on later retrievals, so changed hashes require content comparison before concluding that the record changed. The compact ballot and member responses can be downloaded again from the links above and checked with `tools/check_eu_vote.py`.

| Retrieved response | SHA-256 |
| --- | --- |
| `civic-eu-one-event.json` | `6a93610e719d96ad6033771b89b3662f893e93b41e21c330455757e40828c7ae` |
| `civic-eu-ferber-person.json` | `f0834c5771115ee2ec882680a7487ff8f5ed9a1895bd3b1c44374d9dab984f67` |
| `civic-eu-referral.json` | `7ca96f038faa1a7f301176b56f9d54170edf25cad8c5293f9c3e50e8a1388268` |
| `civic-eu-api-decisions.json` | `1e5ba0a5c5f7b8a677f62a4b6c75e0c6872c471872b34a767e9e94d561e1a963` |
| `civic-eu-api-votes.json` | `099dc0607661aac782fa02a0a5b357950fb3dc5cca0b3fedb87794386805d266` |

