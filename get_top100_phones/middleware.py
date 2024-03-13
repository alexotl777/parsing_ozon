from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging

logger = logging.getLogger(__name__)

class ProxyMiddleware:
    def process_request(self, request, spider):
        proxy = '208.73.236.1:8080'
        if proxy:
            request.meta['proxy'] = proxy

class SeleniumMiddleware:
    def process_request(self, request, spider):
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0")
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(request.url)
        body = str.encode(driver.page_source)

        return HtmlResponse(
            driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )
