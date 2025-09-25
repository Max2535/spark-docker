import asyncio
import random
import time
from typing import Dict

import requests
from playwright.async_api import async_playwright
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def _random_user_agent() -> str:
    uas = [
        # A few up-to-date, commonly seen desktop UAs
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    ]
    return random.choice(uas)


def _realistic_headers() -> Dict[str, str]:
    return {
        "User-Agent": _random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "th-TH,th;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.google.com/",
        # Client hints similar to Chrome
        "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
    }


import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import json
import os
from urllib.parse import urljoin, urlparse

def download_static_content(url, output_file, headers=None):
    """Download static HTML content with better error handling"""
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'th-TH,th;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    try:
        print(f"Downloading static content from: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(response.text)
        
        print(f"✓ Successfully downloaded static HTML to {output_file} ({len(response.text)} chars)")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error downloading static content: {e}")
        return False

def download_dynamic_content(url, output_file, wait_time=10, extra_wait=5):
    """Download JavaScript-rendered content with enhanced waiting and content detection"""
    
    # Configure Chrome options for better content loading
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Add Thai language support
    chrome_options.add_argument('--lang=th-TH')
    chrome_options.add_experimental_option('prefs', {
        'intl.accept_languages': 'th-TH,th,en-US,en'
    })
    
    driver = None
    try:
        print(f"Launching Chrome browser for: {url}")
        driver = webdriver.Chrome(options=chrome_options)
        
        # Set user agent to avoid detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("Loading page...")
        driver.get(url)
        
        # Wait for basic page structure
        try:
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("✓ Basic page structure loaded")
        except TimeoutException:
            print("⚠ Timeout waiting for body, continuing...")
        
        # Wait for specific Shopee elements that indicate content is loaded
        content_selectors = [
            '[data-testid="home-page"]',
            '.shopee-header',
            '.page-product',
            '.home-page',
            'main',
            '.shopee-main'
        ]
        
        content_loaded = False
        for selector in content_selectors:
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                print(f"✓ Content element found: {selector}")
                content_loaded = True
                break
            except TimeoutException:
                continue
        
        if not content_loaded:
            print("⚠ No specific content selectors found, using generic wait")
        
        # Additional wait for dynamic content and images
        print(f"Waiting {extra_wait} seconds for dynamic content to fully load...")
        time.sleep(extra_wait)
        
        # Scroll to trigger lazy loading
        print("Scrolling to trigger lazy-loaded content...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        
        # Get page source after all content is loaded
        page_source = driver.page_source
        
        # Save to HTML file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(page_source)
        
        print(f"✓ Successfully downloaded dynamic HTML to {output_file} ({len(page_source)} chars)")
        return True
        
    except WebDriverException as e:
        print(f"✗ WebDriver error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error downloading dynamic content: {e}")
        return False
    finally:
        if driver:
            driver.quit()
            print("✓ Browser closed")

def download_shopee_to_html_static():
    """Download static HTML content (faster but limited)"""
    url = "https://shopee.co.th/"
    return download_static_content(url, 'shopee_thailand_static.html')

def download_shopee_to_html_dynamic():
    """Download full JavaScript-rendered content (slower but complete)"""
    url = "https://shopee.co.th/"
    return download_dynamic_content(url, 'shopee_thailand_dynamic.html', wait_time=15, extra_wait=8)
    """ดาวน์โหลด HTML แบบ Static พร้อมตั้งค่า Header ให้เหมือนเบราว์เซอร์จริง เพื่อลดการโดนบล็อก"""
    url = "https://shopee.co.th/"

    try:
        sess = requests.Session()
        sess.headers.update(_realistic_headers())
        # Robust retries with backoff for 429/5xx
        retries = Retry(
            total=3,
            backoff_factor=0.6,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            raise_on_status=False,
        )
        sess.mount("https://", HTTPAdapter(max_retries=retries))
        sess.mount("http://", HTTPAdapter(max_retries=retries))

        # เล็กน้อย: หน่วงเวลาแบบสุ่มให้เหมือนคนใช้งาน
        time.sleep(random.uniform(0.8, 2.0))

        resp = sess.get(url, timeout=30)
        resp.raise_for_status()

        with open("shopee_thailand_static.html", "w", encoding="utf-8") as f:
            f.write(resp.text)

        print("Successfully downloaded static HTML to shopee_thailand_static.html")
    except requests.RequestException as e:
        print(f"Error downloading page: {e}")

async def _download_dynamic_with_playwright(url: str, out_path: str) -> None:
    # ใช้ Playwright พร้อมปรับแต่ง context เพื่อลดการถูกตรวจจับ
    async with async_playwright() as p:
        launch_args = dict(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--lang=th-TH,th",
            ],
        )
        try:
            # Prefer system Chrome if available to improve fingerprint realism
            browser = await p.chromium.launch(channel="chrome", **launch_args)
        except Exception:
            browser = await p.chromium.launch(**launch_args)

        # สุ่มค่าหน้าจอให้ดูเหมือนผู้ใช้จริง
        viewports = [(1366, 768), (1536, 864), (1920, 1080)]
        width, height = random.choice(viewports)

        context = await browser.new_context(
            user_agent=_random_user_agent(),
            viewport={"width": width, "height": height},
            locale="th-TH",
            timezone_id="Asia/Bangkok",
            color_scheme="light",
            java_script_enabled=True,
        )

        # ปรับค่า JS บางอย่างให้ดูเหมือนเบราว์เซอร์ปกติ
        await context.add_init_script(
            """
            // navigator.webdriver -> undefined
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            // language & plugins
            Object.defineProperty(navigator, 'languages', { get: () => ['th-TH','th','en-US','en'] });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
            // Chrome runtime
            window.chrome = { runtime: {} };
            // Permissions API mock (for notifications)
            const originalQuery = window.navigator.permissions?.query;
            if (originalQuery) {
              window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ? Promise.resolve({ state: 'denied' }) : originalQuery(parameters)
              );
            }
            """
        )

        page = await context.new_page()
        # เพิ่ม Header เพิ่มเติมที่มักพบในเบราว์เซอร์จริง
        await page.set_extra_http_headers({
            "Accept-Language": "th-TH,th;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://www.google.com/",
        })

        # หน่วงเวลาสุ่มก่อนเข้าเว็บ
        await asyncio.sleep(random.uniform(0.8, 1.8))

        # เข้าเว็บและรอจนโหลดเน็ตเวิร์กค่อนข้างนิ่ง
        await page.goto(url, wait_until="domcontentloaded", timeout=45000)

        # จัดการ consent / region popups ที่พบบ่อยแบบ best-effort
        try:
            for name in ["ตกลง", "ยอมรับ", "ยอมรับทั้งหมด", "ปิด", "Accept All", "OK"]:
                btn = await page.get_by_role("button", name=name)
                if await btn.count() > 0:
                    await btn.first.click(timeout=2000)
                    await asyncio.sleep(0.5)
        except Exception:
            pass

        # เลื่อนหน้าจอแบบสุ่มเพื่อให้เว็บโหลด Lazy content และดูเหมือนมนุษย์
        for _ in range(random.randint(2, 4)):
            await page.mouse.wheel(0, random.randint(600, 1200))
            await asyncio.sleep(random.uniform(0.6, 1.2))

        # รอเนื้อหา dynamic เพิ่มเติมเล็กน้อย
        await asyncio.sleep(random.uniform(2.0, 3.5))

        html = await page.content()
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

        await context.close()
        await browser.close()


def download_shopee_to_html_dynamic():
    """ดาวน์โหลด HTML แบบ Dynamic ด้วย Playwright พร้อมเทคนิคลดการถูกบล็อก"""
    url = "https://shopee.co.th/"
    try:
        asyncio.run(_download_dynamic_with_playwright(url, "shopee_thailand_dynamic.html"))
        print("Successfully downloaded dynamic HTML to shopee_thailand_dynamic.html")
    except Exception as e:
        print(f"Error downloading page: {e}")

def download_with_options():
    """Interactive download with options"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Download web content (static or dynamic)")
    parser.add_argument('--url', default='https://shopee.co.th/', help='URL to download')
    parser.add_argument('--mode', choices=['static', 'dynamic', 'both'], default='both', 
                       help='Download mode: static (fast), dynamic (complete), or both')
    parser.add_argument('--output-dir', default='.', help='Output directory')
    parser.add_argument('--wait-time', type=int, default=15, help='Wait time for page load (seconds)')
    parser.add_argument('--extra-wait', type=int, default=8, help='Extra wait for dynamic content (seconds)')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Generate output filenames
    domain = urlparse(args.url).netloc.replace('.', '_')
    static_file = os.path.join(args.output_dir, f'{domain}_static.html')
    dynamic_file = os.path.join(args.output_dir, f'{domain}_dynamic.html')
    
    results = {}
    
    if args.mode in ['static', 'both']:
        print("=" * 50)
        print("DOWNLOADING STATIC CONTENT")
        print("=" * 50)
        results['static'] = download_static_content(args.url, static_file)
    
    if args.mode in ['dynamic', 'both']:
        print("\n" + "=" * 50)
        print("DOWNLOADING DYNAMIC CONTENT") 
        print("=" * 50)
        results['dynamic'] = download_dynamic_content(
            args.url, dynamic_file, 
            wait_time=args.wait_time, 
            extra_wait=args.extra_wait
        )
    
    # Summary
    print("\n" + "=" * 50)
    print("DOWNLOAD SUMMARY")
    print("=" * 50)
    for mode, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{mode.upper()}: {status}")
    
    # Show file sizes
    for file_path in [static_file, dynamic_file]:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"{os.path.basename(file_path)}: {size:,} bytes")

if __name__ == "__main__":
    download_with_options()