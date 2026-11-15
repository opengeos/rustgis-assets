# Sample data

Natural Earth 1:110m vector data (public domain), trimmed to a few attributes. RustGIS
embeds these at build time for its World Atlas sample project and basemap outline.
`countries_chn.geojson` replaced `countries.geojson` in China in releases that embedded it; it is
kept for building them.

| File | Source | Licence |
| --- | --- | --- |
| `countries.geojson` | Natural Earth, Admin 0 – Countries | Public domain |
| `countries_chn.geojson` | Natural Earth, Admin 0 – Countries, China point of view, embedded by RustGIS releases that built it in (1:10m, simplified to 1:110m density; Hong Kong and Macao merged into China) | Public domain |
| `cities.geojson` | Natural Earth, Populated Places (simple) | Public domain |
| `rivers.geojson` | Natural Earth, Rivers + lake centerlines | Public domain |
| `lakes.geojson` | Natural Earth, Lakes | Public domain |

Source: <https://www.naturalearthdata.com/>

## Data cube catalog

`data-cubes.json` is the catalog of data cubes that RustGIS's Data Cubes pane and `cube.catalog`
list (opengeos/RustGIS#683). RustGIS has a copy built in (`crates/tiles/src/cubes.json`) and reads
this one once per run, so a cube can be added or an address fixed without a new release. A list
that doesn't read whole (over 1 MB, more than 500 entries, or an entry that fails the built-in
list's checks) is ignored, and the built-in copy is used. Keep it in step with
`crates/tiles/src/cubes.json`; the entry format is described in RustGIS's
`docs/user-guide/web-data.md`.

## Worldviews

The countries as each of Natural Earth's 31 points of view sees disputed borders aren't kept here:
they are on source.coop, in the `opengeos/data` repository, at two details:

- `https://data.source.coop/opengeos/data/rustgis/worldviews/countries_<code>.geojson`:
  simplified to the size of `countries.geojson` (about 220 KB), the default.
- `https://data.source.coop/opengeos/data/rustgis/worldviews/original/countries_<code>.geojson.gz`:
  Natural Earth's 1:10m shapes with every island and territory (3 MB gzipped, 10 MB unpacked),
  plus `countries_default.geojson.gz`, the 1:10m original of the de facto countries above.

The codes are `arg`, `bdg`, `bra`, `chn`, `deu`, `egy`, `esp`, `fra`, `gbr`, `grc`, `idn`, `ind`,
`isr`, `ita`, `jpn`, `kor`, `mar`, `nep`, `nld`, `pak`, `pol`, `prt`, `pse`, `rus`, `sau`, `swe`,
`tur`, `twn`, `ukr`, `usa`, `vnm`. RustGIS downloads one when it is chosen in Settings ›
Language › Worldview, at the detail chosen there; none is built into the app.

They are made by [`scripts/worldviews.py`](../scripts/worldviews.py) from Natural Earth's 1:10m
Admin 0 Countries (public domain): grouped by each view's own country code, Hong Kong and Macao
joined to mainland China's group, with the attributes of `countries.geojson`. The simplified
version is simplified with mapshaper to that file's vertex density; disputed land with no 1:110m
country (such as Abkhazia in Russia's view, or Bir Tawil) is kept there as its own feature with
Natural Earth's figures when it covers at least 1,500 km². These follow Natural Earth's points of
view; none is an officially reviewed map.
