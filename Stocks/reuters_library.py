from lxml import html
import requests

class ReutersLibrary:
    #=============CONSTANTS=================#

    REUTERS_BASE_URL = 'http://www.reuters.com/finance/stocks/analyst?symbol='
    RATINGS_XPATH = '//td[@class="data dataBold"]/text()'
    CONSENSUS_XPATH = '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[2]/td[1]/text()'  #taken xpath using chrome inbuilt feature
    PREVIOUS_CLOSE_XPATH = '//*[@id="headerQuoteContainer"]/div[3]/div[1]/span[2]/text()'
    REUTERS_OVERVIEW_URL ='http://www.reuters.com/finance/stocks/overview?symbol='
    DIVIDENDS_XPATH = '//*[@id="overallRatios"]/div/div[2]/table/tbody/tr[5]/td[2]/strong/text()'
    PRICE_EARTINGS_XPATH ='//*[@id="companyVsIndustry"]/div/div[2]/table/tbody/tr[2]/td[2]/text()'
    MEAN_LAST_MONTH_XPATH = '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[4]/div[2]/table/tbody/tr[9]/td[3]/text()'
    DESCRIPTION_XPATH = '//*[@id="sectionTitle"]/h1/text()'

    #=================FUNCTIONS=================#

    @staticmethod
    def get_response(stock_name, path=REUTERS_BASE_URL):
        url = path + stock_name
        page = requests.get(url)
        xml = html.fromstring(page.text)
        return xml

    @staticmethod
    def get_stock_values(stock_name):
        base_response = ReutersLibrary.get_response(stock_name)
        overview_response = ReutersLibrary.get_response(stock_name, path=ReutersLibrary.REUTERS_OVERVIEW_URL)
        values = base_response.xpath(ReutersLibrary.RATINGS_XPATH)
        if len(values) < 5:
            return []
        values.append(base_response.xpath(ReutersLibrary.MEAN_LAST_MONTH_XPATH)[0])
        values.append(base_response.xpath(ReutersLibrary.CONSENSUS_XPATH)[0])
        values.append(overview_response.xpath(ReutersLibrary.DIVIDENDS_XPATH)[0])
        values.append(overview_response.xpath(ReutersLibrary.PRICE_EARTINGS_XPATH)[0])
        values.append(base_response.xpath(ReutersLibrary.DESCRIPTION_XPATH)[0])

        return values
