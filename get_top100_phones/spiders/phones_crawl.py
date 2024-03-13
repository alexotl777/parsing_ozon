'''
Парсинг версий ОС телефонов топ 100 по рейтингу в ozon

Для запуска паука ввести в терминале `scrapy crawl phones_crawl -o os_versions.json`
'''
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PhonesCrawlSpider(CrawlSpider):

    name = "phones_crawl"

    custom_settings = {
        'RETRY_TIMES': 5,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 403, 404, 408],
        'DOWNLOADER_MIDDLEWARES': {
            'get_top100_phones.middleware.ProxyMiddleware': 543,
            'get_top100_phones.middleware.SeleniumMiddleware': 600,
        }
    }

    allowed_domains = ["www.ozon.ru"]
    pages = [f"https://www.ozon.ru/category/smartfony-15502/?page={i}&sorting=rating" for i in range(2, 11)]
    start_urls = ["https://www.ozon.ru/category/smartfony-15502/?sorting=rating"] # URL-адреса со страницами поиска
    start_urls.extend(pages)
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='i8v']//a"), callback="parse_item", follow=True),
    )
    count_phones = 0

    def start_requests(self):
        # проходимся по всем страницам поиска через Selenium webdriver
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=15)

    def parse(self, response):
        '''
        Ищем ссылки в карточках товара и проваливаемся в них 
        Затем используя Selenium webdriver проваливаемся в товар
        '''

        driver = response.meta['driver']

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="ju"]'))
        )

        driver.execute_script("window.scrollBy(0, 2000);")
        for link in driver.find_elements(By.XPATH, '//div[@class="ju"]'):
            if self.count_phones >= 100:
                break

            driver.execute_script("window.scrollBy(0, 2000);")

            phone_page_url = link.find_element(By.XPATH, './/a').get_attribute('href')
            yield SeleniumRequest(url=phone_page_url, callback=self.parse_item, wait_time=10)

    def parse_item(self, response):
        '''
        Ищем в характеристиках товара значения характиристики в теге `dd` включающей слово "Версия" в `span`
        Затем генерируем вытянутую версию ОС в виде списка
        '''
        item = {}
        item["phone_model"] = response.xpath('//title/text()').get()

        os_element = response.xpath('//span[contains(text(), "Версия")]/../following-sibling::dd/a')
        if os_element:
            item["os_version"] = os_element.xpath('text()').get()
        else:
            item["os_version"] = None
        self.count_phones += 1
        yield item
