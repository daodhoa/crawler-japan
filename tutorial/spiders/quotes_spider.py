import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['https://www.premierleague.com/tables']

    def parse(self, response):
        tableContent = response.css('tbody.tableBodyContainer.isPL')
        teams = tableContent.css('tr')
        for team in teams:
            position = team.css('td.pos.button-tooltip span.value::text').get()
            if position is not None:
                teamInfo = team.css('td.team')
                teamLink = teamInfo.css('a::attr(href)').get()
                teamShortName = teamInfo.css('a span.short::text').get()
                teamName = teamInfo.css('a span.long::text').get()
                played = team.css('td')[3].re(r'<td>(\w+)</td>')[0]
                won = team.css('td')[4].re(r'<td>(\w+)</td>')[0]
                draw = team.css('td')[5].re(r'<td>(\w+)</td>')[0]
                lost = team.css('td')[6].re(r'<td>(\w+)</td>')[0]
                gf = team.css('td.hideSmall::text').get()
                ga = team.css('td.hideSmall::text')[1].get()
                # gd = team.css('td')[8].re(r'<td>(\w+)</td>')[0]
                points = team.css('td.points::text').get()
                yield dict(position=position, team=dict(short=teamShortName, long=teamName, link=teamLink),
                    played=played, won=won, draw=draw, lost=lost, gf=gf, ga=ga, points=points)

