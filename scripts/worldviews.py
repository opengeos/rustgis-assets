"""Build countries_<pov>.geojson for each of Natural Earth's point-of-view countries.

Natural Earth publishes Admin 0 Countries as each of 31 countries sees disputed borders, at
1:10m only. RustGIS downloads one of these files when someone picks that worldview (from
source.coop: https://data.source.coop/giswqs/opengeos/rustgis/worldviews/), so each is reduced to the size and attributes of data/countries.geojson (the 1:110m countries):

1. Each 1:10m piece is grouped by the view's own country code (``ADM0_A3_<xx>``); Hong Kong and
   Macao join the group holding mainland China, as at 1:110m.
2. The groups are dissolved, islands under 1,500 km² dropped and the shapes simplified with
   mapshaper (``-simplify 1.5% keep-shapes``, 3 decimals), close to the 1:110m vertex density.
3. A group takes the attributes of its largest piece's country in data/countries.geojson. A group
   with no 1:110m country (Abkhazia in Russia's view, Bir Tawil) is kept when it is land next to
   one and covers at least 1,500 km², with Natural Earth's own name and figures; others (small
   islands such as Mauritius) are dropped, as at 1:110m.

Usage:
    python scripts/worldviews.py NE_GEOJSON_DIR OUT_DIR

Then upload OUT_DIR's files to source.coop's giswqs/opengeos repository, under rustgis/worldviews/
(for example ``aws s3 cp OUT_DIR s3://giswqs/opengeos/rustgis/worldviews/ --recursive
--endpoint-url https://data.source.coop`` with that repository's credentials).

NE_GEOJSON_DIR holds ``ne_10m_admin_0_countries_<pov>.geojson`` and
``ne_110m_admin_0_countries.geojson`` from https://github.com/nvkelso/natural-earth-vector
(``geojson/``). Needs geopandas and mapshaper (``npx mapshaper``).
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import geopandas as gpd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# Natural Earth's file code for each point of view, and the suffix of its ADM0_A3 field.
POVS = {
    "arg": "AR", "bdg": "BD", "bra": "BR", "chn": "CN", "deu": "DE", "egy": "EG", "esp": "ES",
    "fra": "FR", "gbr": "GB", "grc": "GR", "idn": "ID", "ind": "IN", "isr": "IL", "ita": "IT",
    "jpn": "JP", "kor": "KO", "mar": "MA", "nep": "NP", "nld": "NL", "pak": "PK", "pol": "PL",
    "prt": "PT", "pse": "PS", "rus": "RU", "sau": "SA", "swe": "SE", "tur": "TR", "twn": "TW",
    "ukr": "UA", "usa": "US", "vnm": "VN",
}

# Pieces too small for 1:110m that belong with mainland China's group, as they do at 1:110m.
WITH_CHINA = {"HKG", "MAC"}
MIN_KM2 = 1500.0
EQUAL_AREA = "ESRI:54034"
FIELDS = ["continent", "economy", "gdp_md", "income_grp", "iso_a3", "name", "pop_est", "region_un", "subregion"]


def small_scale_attributes(ne_dir):
    """Maps each 1:110m country's ADM0_A3 code to its attributes in data/countries.geojson.

    Args:
        ne_dir: Folder holding Natural Earth's ne_110m_admin_0_countries.geojson.

    Returns:
        A dict from ADM0_A3 code to the attributes RustGIS's countries.geojson gives it.
    """
    ne = json.loads((Path(ne_dir) / "ne_110m_admin_0_countries.geojson").read_text())
    code_of = {f["properties"]["NAME"]: f["properties"]["ADM0_A3"] for f in ne["features"]}
    ours = json.loads((DATA / "countries.geojson").read_text())
    out = {}
    for f in ours["features"]:
        props = f["properties"]
        code = code_of.get(props["name"])
        if code is None:
            raise SystemExit(f"countries.geojson: {props['name']} isn't in Natural Earth's 1:110m file")
        out[code] = props
    return out


def own_attributes(row):
    """The attributes of a group with no 1:110m country, from Natural Earth's own fields.

    Args:
        row: The group's largest 1:10m piece (a GeoDataFrame row).

    Returns:
        A dict with the same fields as data/countries.geojson.
    """
    def number(v):
        v = v.item() if hasattr(v, "item") else v
        return None if v is None or v != v or v < 0 else v

    return {
        "continent": row["CONTINENT"],
        "economy": row["ECONOMY"],
        "gdp_md": number(row["GDP_MD"]),
        "income_grp": row["INCOME_GRP"],
        "iso_a3": "-99",
        "name": row["NAME"],
        "pop_est": number(row["POP_EST"]),
        "region_un": row["REGION_UN"],
        "subregion": row["SUBREGION"],
    }


def build(pov, ne_dir, attrs, work, out_dir):
    """Builds one worldview's countries file.

    Args:
        pov: Natural Earth's point-of-view code, such as "ind".
        ne_dir: Folder holding Natural Earth's GeoJSON files.
        attrs: The 1:110m attributes by ADM0_A3 code, from small_scale_attributes.
        work: A scratch folder.
        out_dir: The folder the file is written to.

    Returns:
        The number of features and vertices written.
    """
    field = "ADM0_A3_" + POVS[pov]
    g = gpd.read_file(Path(ne_dir) / f"ne_10m_admin_0_countries_{pov}.geojson")
    china = g.loc[g["ADM0_A3"] == "CHN", field]
    china_group = china.iloc[0] if len(china) else "CHN"
    g["K"] = [china_group if a in WITH_CHINA else k for a, k in zip(g["ADM0_A3"], g[field])]
    # Each group's attributes: its largest piece's 1:110m country, else Natural Earth's own.
    g["km2"] = g.to_crs(EQUAL_AREA).area / 1e6
    props, unknown = {}, []
    for key, part in g.groupby("K"):
        part = part.sort_values("km2", ascending=False)
        known = [a for a in part["ADM0_A3"] if a in attrs]
        if known:
            props[key] = attrs[known[0]]
        elif part["km2"].sum() >= MIN_KM2 and isinstance(part.iloc[0]["NAME"], str):
            unknown.append((key, own_attributes(part.iloc[0])))
    # A group with no 1:110m country is kept only on land next to one (disputed land such as
    # Abkhazia); islands without one, such as Mauritius, aren't in the 1:110m countries either.
    known_land = g[g["K"].isin(props)].union_all()
    for key, p in unknown:
        if g[g["K"] == key].buffer(0.01).intersects(known_land).any():
            props[key] = p
    src, out = Path(work) / f"{pov}_in.geojson", Path(work) / f"{pov}_out.geojson"
    g[["K", "geometry"]].to_file(src, driver="GeoJSON")
    subprocess.run(
        ["npx", "--yes", "mapshaper@0.7.101", "-i", str(src), "-dissolve2", "K",
         "-filter-islands", "min-area=1500km2", "remove-empty", "-simplify", "1.5%", "keep-shapes",
         "-o", str(out), "precision=0.001", "format=geojson"],
        check=True, capture_output=True,
    )
    shapes = json.loads(out.read_text())["features"]
    features = []
    for f in shapes:
        p = props.get(f["properties"]["K"])
        if p is not None and f["geometry"] is not None:
            features.append({"type": "Feature", "properties": {k: p[k] for k in FIELDS}, "geometry": f["geometry"]})
    features.sort(key=lambda f: f["properties"]["name"])
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    text = json.dumps({"type": "FeatureCollection", "features": features}, separators=(",", ":"), ensure_ascii=False)
    (out_dir / f"countries_{pov}.geojson").write_text(text + "\n")
    vertices = text.count("],[") + len(features)
    return len(features), vertices


def main():
    """Builds every worldview from the Natural Earth folder into the output folder named."""
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    attrs = small_scale_attributes(sys.argv[1])
    with tempfile.TemporaryDirectory() as work:
        for pov in POVS:
            n, v = build(pov, sys.argv[1], attrs, work, sys.argv[2])
            print(f"{pov}: {n} countries, ~{v} vertices")


if __name__ == "__main__":
    main()
