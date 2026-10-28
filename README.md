# rustgis-assets

Static assets for [RustGIS](https://github.com/opengeos/RustGIS), published via GitHub Pages at
**<https://assets.rustgis.app/>**.

Any file committed to `main` is served at the matching path:

```
repo:   images/hero.webp
url:    https://assets.rustgis.app/images/hero.webp
```

## Layout

| Directory | Contents                                   |
| --------- | ------------------------------------------ |
| `images/` | Screenshots, logos and other images         |
| `data/`   | Sample datasets (Natural Earth GeoJSON) and the data cube catalog |
| `fonts/`  | CJK fonts for the web app (Noto Sans, OFL)  |

## Adding files

```bash
git clone https://github.com/opengeos/rustgis-assets.git
cd rustgis-assets
cp /path/to/file images/
git add images/file
git commit -m "Add file"
git push
```

Deployment runs automatically on push to `main` and usually completes within a minute.

## Notes

- Keep individual files under **100 MB** (GitHub's hard limit); the published site must stay
  under **1 GB**, and Pages has a soft bandwidth limit of 100 GB/month.
- Prefer optimized formats: WebP or AVIF for images.
- Screenshots of RustGIS are rendered with its headless harness:
  `cargo run --release -p rustgis-ui-egui --example ui_shot -- script.jsonl` (in the RustGIS
  repo), then converted to WebP.
- `.nojekyll` is present so files and directories beginning with `_` are served as-is.
- Files here are public and cached by GitHub's CDN. Do not commit anything secret, and treat
  published paths as permanent — renaming a file breaks anything already pointing at it.

## License

Released under the [Apache License 2.0](LICENSE). Individual datasets may carry their own
licenses; see the accompanying `README` or `LICENSE` file within each directory where
applicable.
