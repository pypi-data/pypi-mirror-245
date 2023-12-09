import asyncio

from spider_rs import Website

class HttpHeaders:
    def __init__(self, a):
        self.authorization = a

async def main():
    Headers = HttpHeaders("R8")
    website = Website("https://choosealicense.com", False).with_headers(Headers)
    # website.crawl()
    print(website.get_configuration_headers())

asyncio.run(main())