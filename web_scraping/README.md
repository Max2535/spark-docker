# Complete Web Scraping Suite

This directory contains a comprehensive web scraping solution with multiple methods for different use cases:

## 🚀 Quick Start

```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Run all scraping methods
python scraper.py --url https://shopee.co.th/ --method all

# Run specific method
python scraper.py --url https://shopee.co.th/ --method cypress
python scraper.py --url https://shopee.co.th/ --method playwright
python scraper.py --url https://shopee.co.th/ --method selenium
python scraper.py --url https://shopee.co.th/ --method requests
```

## 📋 Available Methods

### 1. 🎯 Cypress (Recommended for JavaScript-heavy sites)
- **Best for**: Single-page applications, dynamic content, e-commerce sites
- **Pros**: Excellent JavaScript handling, browser automation, screenshot/video capabilities
- **Cons**: Slower execution, requires Node.js
- **Use case**: Shopee, React apps, complex JavaScript sites

```bash
# Direct Cypress usage
npx cypress run --project . --browser chrome

# Via unified scraper
python scraper.py --method cypress --url https://shopee.co.th/
```

### 2. 🎭 Playwright (Recommended for async Python workflows)  
- **Best for**: Modern web apps, cross-browser testing, headless automation
- **Pros**: Fast, modern API, excellent documentation, anti-detection features
- **Cons**: Larger installation size
- **Use case**: Modern SPAs, multi-browser scraping

```bash
# Install Playwright browsers
playwright install

# Use via scraper
python scraper.py --method playwright --url https://example.com/
```

### 3. 🔧 Selenium (Traditional browser automation)
- **Best for**: Legacy compatibility, specific browser requirements
- **Pros**: Mature ecosystem, extensive documentation
- **Cons**: Slower than Playwright, more resource intensive
- **Use case**: Legacy systems, specific WebDriver needs

```bash
python scraper.py --method selenium --url https://example.com/
```

### 4. 📄 Requests (Static content only)
- **Best for**: Simple HTML pages, APIs, static content
- **Pros**: Very fast, lightweight, simple
- **Cons**: No JavaScript execution
- **Use case**: Simple websites, server-side rendered content

```bash
python scraper.py --method requests --url https://example.com/
```

## 🛠️ Features

### Anti-Detection Measures
All methods include sophisticated anti-detection techniques:
- Realistic user agents and headers
- Navigator property modifications
- Random delays and human-like scrolling
- Viewport randomization
- Language and timezone spoofing

### Content Handling
- **Consent popups**: Automatic detection and clicking
- **Lazy loading**: Scrolling to trigger content loading
- **Dynamic content**: Waiting for JavaScript execution
- **Error handling**: Robust error recovery

### Output Options
- HTML files with full page content
- JSON reports comparing all methods
- File size and performance metrics
- Screenshots (Cypress only)

## 📁 File Structure

```
web_scraping/
├── scraper.py                    # Unified scraping interface
├── cypress/
│   ├── e2e/
│   │   └── download_html.cy.js  # Cypress test
│   └── support/
│       ├── commands.js          # Custom Cypress commands
│       └── e2e.js              # Global configuration
├── cypress.config.js           # Cypress configuration
├── main.py                     # Playwright quote scraper
├── download_js_to_html.py      # Multiple scraping methods
├── package.json               # Node.js dependencies
└── requirements.txt           # Python dependencies
```

## 🔧 Configuration

### Cypress Configuration (`cypress.config.js`)
```javascript
module.exports = {
  e2e: {
    defaultCommandTimeout: 20000,
    pageLoadTimeout: 90000,
    chromeWebSecurity: false,
    experimentalModifyObstructiveThirdPartyCode: true,
    env: {
      URL: 'https://shopee.co.th/',
      OUT: 'shopee_thailand_cypress.html'
    }
  }
}
```

### Custom Environment Variables
```bash
# For Cypress
export CYPRESS_URL="https://your-target-site.com/"
export CYPRESS_OUT="output_filename.html"

# For unified scraper
python scraper.py --url https://your-site.com/ --output-dir ./results/
```

## 📊 Performance Comparison

| Method     | Speed | JS Support | Anti-Detection | Use Case |
|-----------|-------|------------|----------------|----------|
| Requests  | ⚡⚡⚡⚡ | ❌ | ⚡ | Static sites |
| Selenium  | ⚡⚡ | ✅ | ⚡⚡⚡ | Legacy compatibility |
| Playwright| ⚡⚡⚡ | ✅ | ⚡⚡⚡⚡ | Modern web apps |
| Cypress   | ⚡⚡ | ✅ | ⚡⚡⚡⚡ | Complex SPAs |

## 🎯 Real-World Examples

### E-commerce Sites (Shopee, Lazada)
```bash
python scraper.py --method cypress --url https://shopee.co.th/
```

### News Sites
```bash
python scraper.py --method requests --url https://www.bbc.com/
```

### Social Media (Public Pages)
```bash
python scraper.py --method playwright --url https://example-social-site.com/
```

### API Endpoints
```bash
python scraper.py --method requests --url https://api.example.com/data
```

## 🚨 Best Practices

### Rate Limiting
- Add delays between requests
- Respect robots.txt
- Use residential proxies if needed

### Legal Compliance
- Check website terms of service
- Respect copyright and data protection laws
- Don't overload servers

### Error Handling
- Implement retry mechanisms
- Handle network timeouts gracefully
- Log errors for debugging

## 🔍 Troubleshooting

### Common Issues

**Cypress Test Fails**
```bash
# Check Node.js version
node --version

# Reinstall dependencies
npm install

# Clear Cypress cache
npx cypress cache clear
npx cypress install
```

**Playwright Issues**
```bash
# Install browsers
playwright install

# Update Playwright
pip install -U playwright
```

**Chrome Driver Issues**
```bash
# Update Chrome and ChromeDriver
# For macOS:
brew install --cask google-chrome
brew install chromedriver
```

**Anti-Bot Detection**
- Use residential proxies
- Rotate user agents
- Add longer delays
- Use session cookies

## 📈 Advanced Usage

### Batch Scraping
```python
urls = [
    'https://site1.com/',
    'https://site2.com/',
    'https://site3.com/'
]

for url in urls:
    scraper = WebScraper(url, f"output_{urlparse(url).netloc}")
    result = scraper.scrape_with_playwright()
    print(f"Scraped {url}: {result['success']}")
```

### Custom Headers
```python
# Modify scraper.py to add custom headers
headers = {
    'Authorization': 'Bearer your-token',
    'Custom-Header': 'custom-value'
}
```

### Proxy Support
```python
# Add proxy configuration to browser contexts
context = await browser.new_context(
    proxy={
        'server': 'http://proxy-server:port',
        'username': 'username',
        'password': 'password'
    }
)
```

## การติดตั้ง Dependencies

```bash
# ติดตั้ง Python packages
python3 -m pip install --user -r web_scraping/requirements.txt

# ติดตั้ง Playwright browsers (สำหรับ main.py และ download_js_to_html.py)
python3 -m playwright install

# ChromeDriver จะถูกติดตั้งอัตโนมัติโดย Selenium
```

## การใช้งาน download_js_to_html.py (Playwright)

### พื้นฐาน - ดาวน์โหลด Shopee Thailand
```bash
# ดาวน์โหลดทั้ง static และ dynamic content
python3 web_scraping/download_js_to_html.py

# ดาวน์โหลดเฉพาะ static content (เร็ว)
python3 web_scraping/download_js_to_html.py --mode static

# ดาวน์โหลดเฉพาะ dynamic content (ครบถ้วน)
python3 web_scraping/download_js_to_html.py --mode dynamic
```

### ขั้นสูง - กำหนด URL และตัวเลือกเอง
```bash
# ดาวน์โหลดเว็บไซต์อื่น
python3 web_scraping/download_js_to_html.py --url "https://example.com" --mode both

# ปรับเวลารอให้เหมาะกับเว็บไซต์ที่ช้า
python3 web_scraping/download_js_to_html.py --wait-time 20 --extra-wait 10

# กำหนดโฟลเดอร์สำหรับบันทึกไฟล์
python3 web_scraping/download_js_to_html.py --output-dir downloads/
```

### พารามิเตอร์ทั้งหมด
- `--url`: URL ที่ต้องการดาวน์โหลด (default: https://shopee.co.th/)
- `--mode`: โหมดการดาวน์โหลด static/dynamic/both (default: both)
- `--output-dir`: โฟลเดอร์สำหรับบันทึกไฟล์ (default: ปัจจุบัน)
- `--wait-time`: เวลารอโหลดหน้าเว็บ วินาที (default: 15)
- `--extra-wait`: เวลารอเพิ่มเติมสำหรับ content วินาที (default: 8)

## การใช้งาน main.py (Playwright)

### ดาวน์โหลด quotes
```bash
python3 web_scraping/main.py --mode quotes --url "https://quotes.toscrape.com/"
```

### ดาวน์โหลด table data
```bash
python3 web_scraping/main.py --mode table --url "https://example.com/table" --row-selector "table tr"
```

## ความแตกต่างระหว่าง Static และ Dynamic

### Static Content
- **เร็ว**: ใช้ requests ดาวน์โหลดได้เร็ว
- **จำกัด**: ได้เฉพาะ HTML ที่เซิร์ฟเวอร์ส่งมา ไม่มี JavaScript rendering
- **เหมาะสำหรับ**: เว็บไซต์แบบเก่า, content ที่ไม่ต้องใช้ JavaScript

### Dynamic Content  
- **ครบถ้วน**: ใช้ Playwright เปิด Chromium/Chrome จริง
- **ช้ากว่า**: ต้องรอให้ JavaScript ทำงานเสร็จ
- **เหมาะสำหรับ**: เว็บไซต์สมัยใหม่, SPA, content ที่โหลดด้วย JavaScript

## การปรับปรุงที่เพิ่มเข้ามา

1. **การรอ content ที่ดีขึ้น**: รอหา elements เฉพาะของ Shopee
2. **Scrolling**: เลื่อนหน้าเพื่อ trigger lazy loading
3. **User Agent ที่ดีกว่า**: จำลอง browser จริงๆ
4. **Error handling**: จัดการ timeout และ error ได้ดีขึ้น
5. **Command line options**: ปรับแต่งได้ง่าย
6. **ภาษาไทย**: รองรับการแสดงผลภาษาไทย

## ใช้ Cypress บันทึก HTML แบบเรนเดอร์แล้ว (ตัวเลือกเสริม)

กรณีอยากใช้เบราว์เซอร์จริงผ่าน Cypress เพื่อเปิดหน้าเว็บ, คลิก consent, เลื่อนหน้า แล้วบันทึก HTML:

1) ติดตั้ง Cypress (ครั้งแรก)
```bash
cd web_scraping
npm i -D cypress
```

2) รันแบบ headless หรือ headed
```bash
# headless (เร็วกว่า)
npx cypress run --project . --browser chrome

# หรือเปิด UI / โหมด headed เพื่อตรวจดู
npx cypress run --project . --browser chrome --headed
```

3) เปลี่ยน URL/ไฟล์ผลลัพธ์ได้ผ่าน env
```bash
npx cypress run --project . --browser chrome \
  --env URL="https://shopee.co.th/",OUT="web_scraping/shopee_thailand_cypress.html"
```

สคริปต์หลักอยู่ที่ `web_scraping/cypress/e2e/download_html.cy.js` ซึ่งจะ:
- ตั้ง viewport แบบสุ่ม
- พยายามคลิกปุ่มยินยอม/ปิด consent ที่พบบ่อย
- เลื่อนหน้า (scroll) เพื่อกระตุ้น lazy-load
- บันทึก DOM ปัจจุบันเป็นไฟล์ HTML ที่กำหนด

## ตัวอย่างผลลัพธ์

หลังจากรันแล้วจะได้ไฟล์:
- `shopee_co_th_static.html` - เนื้อหาแบบ static
- `shopee_co_th_dynamic.html` - เนื้อหาแบบ dynamic (ใหญ่กว่า มีข้อมูลครบ)

## Tips

1. **เว็บไซต์ช้า**: เพิ่ม `--wait-time` และ `--extra-wait`
2. **Content ไม่ครบ**: ใช้โหมด `dynamic` และเพิ่มเวลารอ
3. **หน่วยความจำ**: ปิดเบราว์เซอร์อื่นๆ เมื่อใช้โหมด dynamic
4. **การดีบัก**: เอา `--headless` ออกใน Chrome options เพื่อดูเบราว์เซอร์ทำงาน
5. ถ้าใช้ Cypress แล้วเจอการป้องกัน: ลองรันโหมด headed (`--headed`) และปรับดีเลย์/จำนวนครั้งที่เลื่อนหน้ามากขึ้น

## Troubleshooting

### Chrome/ChromeDriver ไม่ทำงาน
```bash
# ติดตั้ง Chrome ใหม่หรือ update ChromeDriver
brew install --cask google-chrome  # macOS
```

### Memory หมด
- ใช้ `--headless` (เปิดอยู่แล้ว)
- ลด `--wait-time` และ `--extra-wait`
- ปิดแอปอื่นๆ ที่ใช้ RAM มาก

---
หมายเหตุ: โปรดใช้งานตามข้อกำหนด/นโยบายของเว็บไซต์เป้าหมาย และปฏิบัติตามกฎหมาย/จริยธรรมการเก็บข้อมูล
