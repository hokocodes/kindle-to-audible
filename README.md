# kindle-to-audible

Small automation helpers to take **Amazon ASINs** from a Kindle library export and **add matching titles to your Audible wishlist** on [audible.com](https://www.audible.com/) using Chrome and Selenium.

## What you need

- **Python 3.10+** (3.x generally fine)
- **Google Chrome** installed (the script drives Chrome)
- An **Audible.com** account (URLs and sign-in flow are US `audible.com`-oriented)
- A CSV of your Kindle books that includes an **ASIN** column (see below)

## Install

From the repo root:

```bash
pip install selenium webdriver-manager
```

On first run, `webdriver-manager` may download a matching ChromeDriver.

## Kindle CSV format

`add_to_audible_wishlist.py` reads **`kindle_books.csv`** by default. The file should:

1. Have a **header row** (the first data row is skipped as the header).
2. Put the **ASIN in the first column**, for example:

| ASIN | Title | Author | … |
|------|--------|--------|---|
| B00XXXXXXX | My book | … | … |

The sample layout in this repo matches `kindle_books.csv` (`ASIN`, `Title`, `Author`, `PurchaseDate`).

## Run the wishlist automation

```bash
python add_to_audible_wishlist.py
```

What happens:

1. Chrome opens and goes to the Audible sign-in page.
2. **You sign in manually** in the browser. The script waits until it sees the signed-in experience (it looks for the word `Explore` in the page).
3. For each ASIN in the CSV, it opens Audible home, searches by ASIN, opens the first result, uses **More options**, then **Add to Wish List** if that control is present.
4. There is a **2 second pause** between books to reduce hammering the site.
5. At the end it prints how many succeeded and lists any **failed ASINs**.

If Audible changes IDs or layout (`header-search`, `results-item-0`, `discovery_buyBox_moreOptions`, `adbl-add-to-wishlist-button`), the selectors in `add_to_audible_wishlist.py` may need updating.

## Optional: `fix_csv.py`

`fix_csv.py` is a minimal template for reading one CSV and writing another (`input.csv` → `output.csv`). Edit the filenames and row logic if you need to reshape an export before feeding `kindle_books.csv`. The checked-in file may be incomplete; treat it as a starting point.

## Caveats

- **Not all Kindle ASINs have an Audible edition**; search or wishlist actions can fail for those rows.
- **Regional stores**: this flow targets **audible.com**. Other regions may need different URLs and flows.
- **Terms of use**: use reasonable delays and your own account; automation may conflict with site terms—use at your own discretion.
