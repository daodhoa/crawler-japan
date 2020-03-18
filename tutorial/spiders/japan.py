import scrapy


class QuotesSpider(scrapy.Spider):
    name = "japan"
    start_urls = ['#']

    def parse(self, response):
        tests = response.css('form p')
        page_tests = dict()
        for test in tests:
            question = test.css('p::text').get()
            number = question[:2].replace('.', '')
            answers = test.css('p').re(r'<br>\n(\w+)<br>|<input .*> (\w+)')
            answers = filter(lambda x: x != "", answers)
            answers = list(answers)
            if answers:
                page_tests[number] = dict(number=number, question=question, answers = answers)

        #yield page_tests
        corrects = response.css('body').re(r'Question (\w+: \w+)')
        for correct in corrects:
            index = correct[:2].replace(':', '')
            ans = correct[-1]
            page_tests[index]['correct'] = ans
        yield page_tests
