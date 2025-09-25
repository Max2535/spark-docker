import asyncio
import argparse
from typing import List, Dict

import pandas as pd
from playwright.async_api import async_playwright


async def scrape_quotes(url: str) -> List[Dict[str, str]]:
    """
    Scrape quotes from quotes.toscrape.com-like pages.
    Returns a list of dicts with keys: text, author, tags
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_selector(".quote", timeout=10000)

            quote_rows = await page.query_selector_all(".quote")
            items: List[Dict[str, str]] = []
            for q in quote_rows:
                text_el = await q.query_selector(".text")
                author_el = await q.query_selector(".author")
                tag_els = await q.query_selector_all(".tag")

                text = await text_el.inner_text() if text_el else ""
                author = await author_el.inner_text() if author_el else ""
                tags_list = [await t.inner_text() for t in tag_els] if tag_els else []
                items.append({
                    "text": text.strip(),
                    "author": author.strip(),
                    "tags": ",".join(t.strip() for t in tags_list),
                })
            return items
        finally:
            await browser.close()


async def scrape_table(url: str, selector: str = "table tr") -> List[List[str]]:
    """
    Generic table scraper: collects text for all <td> under row selector.
    Returns list of rows (each row is a list of cell texts).
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_selector(selector, timeout=10000)

            rows = await page.query_selector_all(selector)
            data: List[List[str]] = []
            for row in rows:
                cells = await row.query_selector_all("td, th")
                texts = [
                    (await cell.inner_text()).strip()
                    for cell in cells
                ]
                if any(texts):
                    data.append(texts)
            return data
        finally:
            await browser.close()


async def main():
    parser = argparse.ArgumentParser(description="Simple web scraping to CSV using Playwright")
    parser.add_argument(
        "--mode",
        choices=["quotes", "table"],
        default="quotes",
        help="Scraping mode: 'quotes' (default) or 'table'",
    )
    parser.add_argument(
        "--url",
        default="https://quotes.toscrape.com/",
        help="Target URL (defaults to a demo site that allows scraping)",
    )
    parser.add_argument(
        "--row-selector",
        default="table tr",
        help="CSS selector for table rows when mode=table",
    )
    parser.add_argument(
        "--output",
        default="output.csv",
        help="Output CSV file path",
    )
    args = parser.parse_args()

    if args.mode == "quotes":
        records = await scrape_quotes(args.url)
        df = pd.DataFrame.from_records(records, columns=["text", "author", "tags"])
    else:
        table = await scrape_table(args.url, selector=args.row_selector)
        df = pd.DataFrame(table)

    df.to_csv(args.output, index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    asyncio.run(main())
