# Sample data

Natural Earth 1:110m vector data (public domain), trimmed to a few attributes. RustGIS
embeds these at build time for its World Atlas sample project and basemap outline.
`countries_chn.geojson` replaces `countries.geojson` when RustGIS runs in China.

| File | Source | Licence |
| --- | --- | --- |
| `countries.geojson` | Natural Earth, Admin 0 – Countries | Public domain |
| `countries_chn.geojson` | Natural Earth, Admin 0 – Countries, China point of view (1:10m, simplified to 1:110m density; Hong Kong and Macao merged into China) | Public domain |
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
