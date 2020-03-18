import scrapy


class QuotesSpider(scrapy.Spider):
    name = "japan"
    start = 1
    end = 10

    def start_requests(self):
        main_url = 'https://japanesetest4you.com/japanese-language-proficiency-test-jlpt-n5-vocabulary-exercise-'
        for i in range(self.start, self.end + 1):
            url = main_url + str(i) + '/'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page_number = response.url.split('-')[-1].replace('/', '');
        tests = response.css('form p')
        page_tests = dict()
        for test in tests:
            question = test.css('p::text').get()
            number = question[:2].replace('.', '')
            answers = test.css('p').re(r'<br>\n(\w+)<br>|<input .*> (\w+)')
            answers = filter(lambda x: x != "", answers)
            answers = list(answers)
            if answers:
                page_tests[str(page_number) + '.' + str(number)] = dict(number=number, question=question, answers = answers)

        corrects = response.css('body').re(r'Question (\w+: \w+)')
        for correct in corrects:
            index = correct[:2].replace(':', '')
            ans = correct[-1]
            page_tests[str(page_number) + '.' + str(index)]['correct'] = ans
        yield page_tests
