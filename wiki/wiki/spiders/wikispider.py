import scrapy


class WikispiderSpider(scrapy.Spider):
    name = "wikispider"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_programming_languages"]

    def parse(self, response):
        for li in response.css('div.div-col ul li'):
            name = li.css('a::text').get()
            link = li.css('a::attr(href)').get()
            
            if link:
                full_url = response.urljoin(link)
                yield response.follow(full_url, callback=self.parse_language, meta={'name': name})
    
    def parse_language(self, response):
        name = response.meta['name']
        
        first_paragraph = response.css('p::text').get()
        paradigm = response.xpath('//tr[th[contains(text(), "Paradigm")]]/td//text()').get()
        designed_by = response.xpath('//tr[th[contains(text(), "Designed by")]]/td//text()').get()
        
        yield {
            'name': name,
            'first_paragraph': first_paragraph.strip() if first_paragraph else None,
            'paradigm': paradigm.strip() if paradigm else None,
            'designed_by': designed_by.strip() if designed_by else None,
            'url': response.url
        }
