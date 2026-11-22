# Fonts

Fallback fonts for RustGIS where installed fonts cannot draw the selected language. Browsers
cannot read installed fonts, and phone system fonts are not always available in a readable format.

| File | Font | Licence |
| --- | --- | --- |
| `NotoSansSC-Regular.otf` | Noto Sans SC (Simplified Chinese subset) | SIL Open Font License 1.1 |
| `NotoSansTC-Regular.otf` | Noto Sans TC (Traditional Chinese subset, Taiwan's glyph forms) | SIL Open Font License 1.1 |
| `NotoSansJP-Regular.otf` | Noto Sans JP (Japanese subset) | SIL Open Font License 1.1 |
| `NotoSansKR-Regular.otf` | Noto Sans KR (Korean subset) | SIL Open Font License 1.1 |
| `NotoSans-VF.ttf` | Noto Sans (Latin, Greek and Cyrillic, including Azerbaijani and Vietnamese) | SIL Open Font License 1.1 |
| `NotoSansBengali-VF.ttf` | Noto Sans Bengali | SIL Open Font License 1.1 |
| `NotoSansLao-VF.ttf` | Noto Sans Lao | SIL Open Font License 1.1 |
| `Vazirmatn-Regular.ttf` | Vazirmatn (Arabic script with Latin) | SIL Open Font License 1.1 |

Sources: <https://github.com/notofonts/noto-cjk> (`Sans/SubsetOTF`), licence text [OFL.txt](OFL.txt);
<https://github.com/rastikerdar/vazirmatn> (release v33.003, `fonts/ttf`), licence text
[OFL-Vazirmatn.txt](OFL-Vazirmatn.txt).

The three `-VF.ttf` files are the unmodified variable fonts from
[google/fonts](https://github.com/google/fonts/tree/06bfe0d62a98375cb09c942fa18e68bd32cff057)
(revision `06bfe0d62a98375cb09c942fa18e68bd32cff057`), from `ofl/notosans`, `ofl/notosansbengali`
and `ofl/notosanslao`. Each file's copyright and licence are kept alongside it as
`OFL-NotoSans.txt`, `OFL-NotoSansBengali.txt` and `OFL-NotoSansLao.txt` respectively.
Their default weight is Regular (400); width and weight axes remain available.
