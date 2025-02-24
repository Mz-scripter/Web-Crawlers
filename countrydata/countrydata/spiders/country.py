import scrapy


class CountrySpider(scrapy.Spider):
    name = "country"
    allowed_domains = ["www.scrapethissite.com"]
    start_urls = ["https://www.scrapethissite.com/pages/simple/"]

    def parse(self, response):
        countries = response.css('div.country')
        
        for country in countries:
            yield {
                "Name": " ".join(country.css('h3.country-name::text').getall()).strip(),
                "Capital": country.css('span.country-capital::text').get().strip(),
                "Population": country.css('span.country-population::text').get(),
                "Area": country.css('span.country-area::text').get()
            }
