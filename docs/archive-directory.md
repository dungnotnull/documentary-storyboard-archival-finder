# Public Archive Directory - Documentary Storyboard & Archival Finder

> Authoritative sources for rights-cleared or licensable archival footage and images. Use this directory as the primary crawl target for `tools/knowledge_updater.py` and as a fallback catalog when public archive sites are unreachable.

## Usage
For each required visual in the shot list:
1. Query the most relevant sources below.
2. Open the item's rights/license page (not just the search snippet).
3. Record: source, exact URL, license type, attribution requirement, rights clarity, and access date.
4. If the source is offline, mark the entry with `staleness: fallback directory <date>` and rights clarity `Unclear - verify before use`.

## North America

### Library of Congress - Film and Videos
- Base URL: https://www.loc.gov/film-and-videos/
- Scope: U.S. history, culture, early cinema, newsreels.
- Typical license: Public Domain (pre-1929 or U.S. government); some rights-restricted.
- Search strategy: Use collection facets; inspect "Rights Advisory" and "Part of" fields.
- Example query: `apollo 11 site:loc.gov/film-and-videos`
- Rights page: https://www.loc.gov/legal/
- API: https://www.loc.gov/apis/
- Machine query: `https://www.loc.gov/film-and-videos/?q={query}&fo=json`

### Internet Archive - Prelinger
- Base URL: https://archive.org/details/prelinger
- Scope: Ephemeral, advertising, educational, and industrial films.
- Typical license: Mostly Public Domain or CC; verify per item metadata.
- Search strategy: Use archive.org search; inspect item `licenseurl` and `license` metadata.
- Example query: `prelinger apollo`
- Rights page: https://archive.org/about/terms.php
- API: https://archive.org/services/docs/api/
- Machine query: `https://archive.org/advancedsearch.php?q=collection%3A{collection}+{query}&output=json&rows={n}`

### U.S. National Archives (NARA)
- Base URL: https://catalog.archives.gov/
- Scope: U.S. federal records, military, NASA, presidential libraries.
- Typical license: Public Domain for federal records unless marked otherwise.
- Search strategy: Search catalog; open "Description" and "Access Restrictions".
- Example query: `apollo 11 catalog.archives.gov`
- Rights page: https://www.archives.gov/legal
- API: https://catalog.archives.gov/api/v1/
- Machine query: `https://catalog.archives.gov/api/v1/search?q={query}`

## Europe / Global

### Europeana
- Base URL: https://www.europeana.eu/
- Scope: Cultural heritage from European institutions.
- Typical license: Mixed (PD, CC0, CC-BY, rights-restricted); use rights filters.
- Search strategy: Use `RIGHTS=*creative*` or `RIGHTS=*public*` filters.
- Example query: `apollo site:europeana.eu`
- Rights page: https://pro.europeana.eu/share-your-data/data-guidelines
- API: https://pro.europeana.eu/resources/developers/api
- Machine query: `https://api.europeana.eu/record/v2/search.json?query={query}&rows=12&wskey=APIKEY`

### Wikimedia Commons
- Base URL: https://commons.wikimedia.org/
- Scope: Images, video, audio uploaded by users and GLAM partners.
- Typical license: CC0, CC-BY, CC-BY-SA, Public Domain.
- Search strategy: Filter by license; read file page "Licensing" and "Author".
- Example query: `apollo 11 site:commons.wikimedia.org`
- Rights page: https://commons.wikimedia.org/wiki/Commons:Licensing
- API: https://commons.wikimedia.org/wiki/API:Main_page
- Machine query: `https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={query}&srnamespace=6&format=json`

## Stock / CC0 Aggregators

### Pexels
- Base URL: https://www.pexels.com/
- Scope: Stock photos and videos.
- Typical license: Pexels License - free to use, no attribution required but appreciated.
- Search strategy: Read per-asset license page.
- Example query: `apollo`
- Rights page: https://www.pexels.com/license/

### Pixabay
- Base URL: https://pixabay.com/
- Scope: Stock photos, videos, illustrations.
- Typical license: Pixabay License - free for commercial use, no attribution required.
- Search strategy: Read per-asset license page.
- Example query: `apollo`
- Rights page: https://pixabay.com/service/terms/

## License verification checklist
- [ ] Asset source URL is exact and reachable at access time.
- [ ] License type is read from the item's rights field, not the search snippet.
- [ ] Attribution requirement is recorded if the license requires it.
- [ ] Rights clarity is classified as `Clear`, `Attribution-required`, or `Unclear - do not use without clearance`.
- [ ] Access date is recorded.
- [ ] If the site is offline, a fallback note and staleness flag are added.

## Fallback rule
When any archive site is unreachable, use this directory as the cached source catalog. Mark entries with `fallback directory <date>` and classify rights clarity as `Unclear - verify before use` until the live source can be re-checked.
