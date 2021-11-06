import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://superjob.ru/vacancy/search/?keywords=python&page=1']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@rel='next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//span[@class='_185V- _1_rZy _2ogzo']/a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        link = response.url
        site = self.allowed_domains[0]
        salary = response.xpath("//span[@class='_2Wp8I _185V- _1_rZy Ml4Nx']/text()").getall()
        item = JobparserItem(name=name, link=link, site=site, salary=salary)
        yield item
