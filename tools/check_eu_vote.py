"""Check the published EU vote against downloaded official JSON, offline.

Usage: python3 tools/check_eu_vote.py decision.json member.json
The source URLs and ballot distinction are documented in data/EU-EVIDENCE.md.
"""
import argparse
import json
from pathlib import Path

from snapshot import PLACES

DECISION = 'MTG-PL-2026-11-12-DEC-200101'
OPTIONS = {'had_voter_favor': 'Yes', 'had_voter_against': 'No',
           'had_voter_abstention': 'Abstained'}


def verify(decision_path, member_path):
    decisions = json.loads(decision_path.read_text(encoding='utf-8'))['data']
    members = json.loads(member_path.read_text(encoding='utf-8'))['data']
    ballot = next(row for row in decisions if row.get('activity_id') == DECISION)
    if (ballot['activity_date'] != '2026-11-12'
            or ballot['headingLabel']['en'].strip() != 'Draft legislative act'
            or not ballot['activity_label']['en'].startswith('A10-0271/2026')
            or not ballot['decision_method'].endswith('/VOTE_ELECTRONIC_ROLLCALL')):
        raise ValueError('The record is not the named draft-act ballot reviewed here.')

    count = 0
    for place in PLACES.values():
        level = next(row for row in place['levels'] if row['id'] == 'europe')
        for activity in level.get('activities', []):
            for vote in activity.get('votes', []):
                if vote.get('source_record') != DECISION:
                    raise ValueError('The published vote refers to a different decision.')
                member = next(row for row in members
                              if row.get('identifier') == vote['voter_id'])
                name = member['givenName'] + ' ' + member['familyName']
                person = 'person/' + vote['voter_id']
                marked = [label for field, label in OPTIONS.items()
                          if person in ballot.get(field, [])]
                intended = [field for field, people in ballot.items()
                            if field.startswith('had_voter_intended_') and person in people]
                if name != vote['name'] or marked != [vote['vote']] or intended:
                    raise ValueError('Published name or vote differs from the official record.')
                count += 1
                print(f'{place["name"]}: {name}: {marked[0]} on {DECISION}')
    if not count:
        raise ValueError('No published EU vote found.')
    print(f'{count} published entries matched the official named ballot and member identity.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Verify the snapshot’s named EU vote.')
    parser.add_argument('decision', type=Path, help='Downloaded official decision JSON')
    parser.add_argument('member', type=Path, help='Downloaded official member JSON')
    args = parser.parse_args()
    try:
        verify(args.decision, args.member)
    except (OSError, KeyError, ValueError, StopIteration) as error:
        parser.exit(1, f'Check failed: {error or "record not found"}\n')
