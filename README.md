# Civic Brief · Bobingen and Augsburg

An English snapshot of local decisions and elected representatives. It opens on Bobingen, a city in Augsburg district. Switch to Augsburg for the independent city. Each story links to its source; each profile explains the local connection. Official neighbourhood names stay in German to match the city’s street directory.

The Germany and EU sections include named votes from 12 November 2026. EU coverage explains the party-list system, features a locally connected MEP and links to the full German delegation. The disaster-response proposal remains under negotiation.

**Snapshot date: 14 November 2026.** [Bobingen on a phone](screenshots/bobingen-mobile.png) · [Augsburg on a desktop](screenshots/augsburg-desktop.png) · [Augsburg district lookup](screenshots/augsburg-district.png) · [Federal profile and named vote](screenshots/augsburg-federal.png)

## Run locally

From the folder containing this README, run one command with Python 3:

```sh
python3 -m http.server 8791 --bind 127.0.0.1 --directory docs
```

Open [the local site](http://127.0.0.1:8791/). Press Ctrl+C to stop. If the port is in use, change 8791 in both the command and the address. You can also open `docs/index.html` directly. All pages work offline. Following an external source link requires an internet connection. There is no install step, backend, API key or live AI call.

## Publish on GitHub Pages

1. Copy the contents of this folder to the **root** of a GitHub repository and push them to `main`. The homepage should be at `docs/index.html`.
2. Open **Settings → Pages → Build and deployment**. Select **Deploy from a branch**, choose **main** and **/docs**, then select **Save**.
3. Once deployment finishes, select **Visit site**. A project site normally uses `https://NAME.github.io/REPOSITORY/`. Internal links, images and scripts use relative paths so the site works under that repository path. [GitHub’s publishing instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## Update the snapshot

Edit the date, stories, people and sources in `data/snapshot.json`. Augsburg’s district assignments are in `data/city-districts.json`. Run `python3 tools/render.py`, then `python3 tools/check.py`. Commit the generated pages in `docs/` with the data. The district picker uses `docs/assets/district.js`. All 42 assignments are also available without JavaScript.

Check the official city and district notices weekly. Check agendas before meetings and approved minutes afterwards. For parliamentary stories, check the procedure stage and the named voting record separately. Keep at most three updates per homepage, and record the source publication date separately from the event date. Advance the snapshot date after checking all retained stories and profiles. This routine is manual.

The snapshot covers selected representatives and activities. Council decisions are credited to the council. Individual votes come from official named records. The maps show simplified municipal boundaries. See the [review and known gaps](REVIEW.md), [EU evidence](data/EU-EVIDENCE.md) and [map credits](MAP-LICENSE.md).
