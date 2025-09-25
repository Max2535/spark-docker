#!/usr/bin/env python3
"""
Complete Web Scraping Suite
============================

This script provides multiple methods for web scraping:
1. Cypress - for JavaScript-heavy sites with full browser automation
2. Playwright - for async Python browser automation 
3. Selenium - for traditional browser automation
4. Requests - for simple static content

Usage:
    python scraper.py --method cypress --url https://shopee.co.th/
    python scraper.py --method playwright --url https://shopee.co.th/
    python scraper.py --method selenium --url https://shopee.co.th/
    python scraper.py --method requests --url https://shopee.co.th/
    python scraper.py --method all --url https://shopee.co.th/
"""

import argparse
import asyncio
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


class WebScraper:
    """Complete web scraping suite with multiple methods"""
    
    def __init__(self, url: str, output_dir: str = "output"):
        self.url = url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.domain = urlparse(url).netloc.replace('.', '_')
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def _get_output_path(self, method: str, extension: str = "html") -> Path:
        """Generate output file path"""
        filename = f"{self.domain}_{method}_{self.timestamp}.{extension}"
        return self.output_dir / filename
    
    def scrape_with_requests(self) -> Dict[str, any]:
        """Scrape using requests (static content only)"""
        print(f"🔄 Scraping with requests: {self.url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'th-TH,th;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        try:
            response = requests.get(self.url, headers=headers, timeout=30)
            response.raise_for_status()
            
            output_path = self._get_output_path("requests")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            # Parse with BeautifulSoup for additional info
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "No title"
            
            return {
                'success': True,
                'method': 'requests',
                'output_file': str(output_path),
                'size': len(response.text),
                'title': title,
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type', ''),
                'execution_time': 'Fast (~1-3 seconds)'
            }
            
        except requests.RequestException as e:
            return {
                'success': False,
                'method': 'requests',
                'error': str(e)
            }
    
    def scrape_with_selenium(self) -> Dict[str, any]:
        """Scrape using Selenium (browser automation)"""
        print(f"🔄 Scraping with Selenium: {self.url}")
        
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            # Configure Chrome options
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument('--lang=th-TH')
            
            start_time = time.time()
            driver = webdriver.Chrome(options=chrome_options)
            
            try:
                # Anti-detection
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                driver.get(self.url)
                
                # Wait for body
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                # Scroll to trigger lazy loading
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, 0);")
                
                # Get page source
                page_source = driver.page_source
                title = driver.title
                
                output_path = self._get_output_path("selenium")
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(page_source)
                
                execution_time = time.time() - start_time
                
                return {
                    'success': True,
                    'method': 'selenium',
                    'output_file': str(output_path),
                    'size': len(page_source),
                    'title': title,
                    'execution_time': f"{execution_time:.1f} seconds"
                }
                
            finally:
                driver.quit()
                
        except ImportError:
            return {
                'success': False,
                'method': 'selenium',
                'error': 'Selenium not installed. Run: pip install selenium'
            }
        except Exception as e:
            return {
                'success': False,
                'method': 'selenium',
                'error': str(e)
            }
    
    async def scrape_with_playwright(self) -> Dict[str, any]:
        """Scrape using Playwright (async browser automation)"""
        print(f"🔄 Scraping with Playwright: {self.url}")
        
        try:
            from playwright.async_api import async_playwright
            
            start_time = time.time()
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                        "--lang=th-TH,th",
                    ]
                )
                
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                    viewport={"width": 1920, "height": 1080},
                    locale="th-TH",
                    timezone_id="Asia/Bangkok",
                )
                
                # Anti-detection script
                await context.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                    Object.defineProperty(navigator, 'languages', { get: () => ['th-TH','th','en-US','en'] });
                    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
                    window.chrome = { runtime: {} };
                """)
                
                page = await context.new_page()
                
                # Navigate to page
                await page.goto(self.url, wait_until="domcontentloaded", timeout=45000)
                
                # Handle consent popups
                consent_texts = ["ตกลง", "ยอมรับ", "ยอมรับทั้งหมด", "ปิด", "Accept All", "OK"]
                for text in consent_texts:
                    try:
                        button = page.get_by_role("button", name=text)
                        if await button.count() > 0:
                            await button.first.click(timeout=2000)
                            await asyncio.sleep(0.5)
                    except:
                        continue
                
                # Scroll for lazy loading
                for _ in range(3):
                    await page.mouse.wheel(0, 800)
                    await asyncio.sleep(1)
                
                # Wait for content
                await asyncio.sleep(3)
                
                # Get content
                html = await page.content()
                title = await page.title()
                
                output_path = self._get_output_path("playwright")
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html)
                
                await context.close()
                await browser.close()
                
                execution_time = time.time() - start_time
                
                return {
                    'success': True,
                    'method': 'playwright',
                    'output_file': str(output_path),
                    'size': len(html),
                    'title': title,
                    'execution_time': f"{execution_time:.1f} seconds"
                }
                
        except ImportError:
            return {
                'success': False,
                'method': 'playwright',
                'error': 'Playwright not installed. Run: pip install playwright && playwright install'
            }
        except Exception as e:
            return {
                'success': False,
                'method': 'playwright',
                'error': str(e)
            }
    
    def scrape_with_cypress(self) -> Dict[str, any]:
        """Scrape using Cypress (Node.js browser automation)"""
        print(f"🔄 Scraping with Cypress: {self.url}")
        
        try:
            # Check if cypress is available
            result = subprocess.run(['npx', 'cypress', '--version'], 
                                 capture_output=True, text=True, cwd='.')
            if result.returncode != 0:
                return {
                    'success': False,
                    'method': 'cypress',
                    'error': 'Cypress not installed. Run: npm install cypress'
                }
            
            # Set environment variables for Cypress
            env = os.environ.copy()
            env['CYPRESS_URL'] = self.url
            output_filename = f"{self.domain}_cypress_{self.timestamp}.html"
            env['CYPRESS_OUT'] = output_filename
            
            start_time = time.time()
            
            # Run Cypress test
            result = subprocess.run([
                'npx', 'cypress', 'run', 
                '--project', '.', 
                '--browser', 'chrome',
                '--headless'
            ], env=env, capture_output=True, text=True, cwd='.')
            
            execution_time = time.time() - start_time
            
            # Check if output file was created
            output_path = Path(output_filename)
            if output_path.exists():
                size = output_path.stat().st_size
                
                # Try to extract title from HTML
                try:
                    with open(output_path, 'r', encoding='utf-8') as f:
                        soup = BeautifulSoup(f.read(), 'html.parser')
                        title = soup.title.string if soup.title else "No title"
                except:
                    title = "Could not extract title"
                
                # Move to output directory
                final_output_path = self.output_dir / output_filename
                output_path.rename(final_output_path)
                
                return {
                    'success': True,
                    'method': 'cypress',
                    'output_file': str(final_output_path),
                    'size': size,
                    'title': title,
                    'execution_time': f"{execution_time:.1f} seconds",
                    'cypress_output': result.stdout[-500:] if result.stdout else ""
                }
            else:
                return {
                    'success': False,
                    'method': 'cypress',
                    'error': f"Cypress test failed. Output file not created. Error: {result.stderr}"
                }
                
        except FileNotFoundError:
            return {
                'success': False,
                'method': 'cypress',
                'error': 'Node.js/npm not found. Please install Node.js first.'
            }
        except Exception as e:
            return {
                'success': False,
                'method': 'cypress',
                'error': str(e)
            }
    
    def compare_results(self, results: List[Dict[str, any]]) -> None:
        """Compare results from different scraping methods"""
        print("\n" + "="*80)
        print("📊 SCRAPING RESULTS COMPARISON")
        print("="*80)
        
        successful_results = [r for r in results if r.get('success')]
        failed_results = [r for r in results if not r.get('success')]
        
        if successful_results:
            print(f"\n✅ Successful methods: {len(successful_results)}")
            print("-" * 50)
            
            for result in successful_results:
                print(f"🔹 {result['method'].upper()}:")
                print(f"   📁 File: {result['output_file']}")
                print(f"   📏 Size: {result['size']:,} bytes")
                print(f"   📄 Title: {result.get('title', 'N/A')}")
                print(f"   ⏱️  Time: {result.get('execution_time', 'N/A')}")
                print()
            
            # Find the largest file (likely most complete)
            largest = max(successful_results, key=lambda x: x['size'])
            print(f"🏆 Most complete result: {largest['method'].upper()} ({largest['size']:,} bytes)")
        
        if failed_results:
            print(f"\n❌ Failed methods: {len(failed_results)}")
            print("-" * 50)
            
            for result in failed_results:
                print(f"🔹 {result['method'].upper()}: {result.get('error', 'Unknown error')}")
                print()
        
        # Generate summary report
        self._generate_report(results)
    
    def _generate_report(self, results: List[Dict[str, any]]) -> None:
        """Generate a JSON report of all results"""
        report = {
            'url': self.url,
            'timestamp': self.timestamp,
            'domain': self.domain,
            'total_methods': len(results),
            'successful_methods': len([r for r in results if r.get('success')]),
            'results': results
        }
        
        report_path = self.output_dir / f"{self.domain}_report_{self.timestamp}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Detailed report saved to: {report_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Complete Web Scraping Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scraper.py --method cypress --url https://shopee.co.th/
  python scraper.py --method playwright --url https://example.com/
  python scraper.py --method all --url https://shopee.co.th/
  python scraper.py --url https://shopee.co.th/ --output-dir ./results/
        """
    )
    
    parser.add_argument('--url', default='https://shopee.co.th/', 
                       help='URL to scrape (default: https://shopee.co.th/)')
    parser.add_argument('--method', 
                       choices=['requests', 'selenium', 'playwright', 'cypress', 'all'],
                       default='all',
                       help='Scraping method to use (default: all)')
    parser.add_argument('--output-dir', default='output',
                       help='Output directory (default: output)')
    parser.add_argument('--compare', action='store_true',
                       help='Compare results when using multiple methods')
    
    args = parser.parse_args()
    
    print("🚀 Starting Web Scraping Suite")
    print(f"🎯 Target URL: {args.url}")
    print(f"🔧 Method(s): {args.method}")
    print(f"📁 Output directory: {args.output_dir}")
    print("-" * 80)
    
    scraper = WebScraper(args.url, args.output_dir)
    results = []
    
    if args.method in ['requests', 'all']:
        results.append(scraper.scrape_with_requests())
    
    if args.method in ['selenium', 'all']:
        results.append(scraper.scrape_with_selenium())
    
    if args.method in ['playwright', 'all']:
        result = asyncio.run(scraper.scrape_with_playwright())
        results.append(result)
    
    if args.method in ['cypress', 'all']:
        results.append(scraper.scrape_with_cypress())
    
    # Show comparison if multiple methods or explicitly requested
    if len(results) > 1 or args.compare:
        scraper.compare_results(results)
    else:
        # Show single result
        result = results[0]
        if result.get('success'):
            print(f"\n✅ Successfully scraped with {result['method']}!")
            print(f"📁 Output: {result['output_file']}")
            print(f"📏 Size: {result['size']:,} bytes")
        else:
            print(f"\n❌ Failed to scrape with {result['method']}")
            print(f"❗ Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()