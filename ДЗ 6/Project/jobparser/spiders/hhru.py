import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?fromSearchLine=true&st=searchVacancy&text=python&area=1&search_field=description&search_field=company_name&search_field=name',
                  'https://hh.ru/search/vacancy?fromSearchLine=true&st=searchVacancy&text=python&area=2&search_field=description&search_field=company_name&search_field=name']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1[@data-qa='vacancy-title']/text()").get()
        link = response.url
        site = self.allowed_domains[0]
        salary = response.xpath("//div[@class='vacancy-salary']/span/text()").getall()
        item = JobparserItem(name=name, link=link, site=site, salary=salary)
        yield item