# Civic Brief · Stratford-on-Avon

[Open the public site](https://bttlbmb.github.io/civic-brief/) · [Source repository](https://github.com/Bttlbmb/civic-brief)

A static UK constituency MVP covering recent council decisions, Manuela Perteghella’s voting and parliamentary activity, verified media reporting, representation and practical contact routes.

**Content snapshot: 15 November 2026.** This is an independently curated prototype with linked evidence, not a council or Parliament service or a live feed.

## Published build

GitHub Pages publishes `main:/docs`. The homepage leads with three confirmed decisions; consultations and pending decisions appear below. Representatives leads with MP activity. Service problems and contact actions have their own Who to contact page.

The build contains eleven HTML pages and local assets. Open `docs/index.html` locally or serve the directory with Python:

```sh
python3 -m http.server 8791 --bind 127.0.0.1 --directory docs
```

External evidence links require internet access. Portrait attribution and coverage limits are on the Sources & coverage page.

## Updating

The current published UK snapshot is in `docs/`. Build and check the UK project, then copy its verified static output into this folder and push to `main`.

The earlier German prototype’s research and tools remain in the repository. Its former published pages are preserved in Git history.
