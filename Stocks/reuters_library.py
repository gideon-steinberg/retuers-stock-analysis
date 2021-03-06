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
    
    NZX50_URL = 'http://topforeignstocks.com/indices/components-of-the-nzsx-50-index/'
    NZX_URL = 'https://www.nzx.com/markets/NZSX/securities'

    NZX50_XPATH = '//*[@id="tablepress-915"]/tbody/tr/td[3]/text()'
    NZX_XPATH = '//*[@id="instruments"]/table/tbody/tr/td[1]/a/text()'

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
        basic_values = base_response.xpath(ReutersLibrary.RATINGS_XPATH)
        
        result = {"code" : stock_name}
        if len(basic_values) > 0:
            result["buy"] = basic_values[0] 
            result["outperform"] = basic_values[1] 
            result["hold"] = basic_values[2] 
            result["underperform"] = basic_values[3] 
            result["sell"] = basic_values[4] 
            result["no_opinion"] = basic_values[5] 
            result["mean"] = basic_values[6] 
        
            mean_last_month = base_response.xpath(ReutersLibrary.MEAN_LAST_MONTH_XPATH)[0]
            if mean_last_month == "--":
                mean_last_month = 0
            difference = float(result["mean"]) - float(mean_last_month)
            if difference == 0:
                difference = ""
            else:
                # formatting......
                difference = float(format(difference, '.4f'))
            result["mean_difference"] = difference
            result["consensus"] = base_response.xpath(ReutersLibrary.CONSENSUS_XPATH)[0]
            result["price_earnings"] = overview_response.xpath(ReutersLibrary.PRICE_EARTINGS_XPATH)[0].strip()
        
        parsed_output = overview_response.xpath(ReutersLibrary.DIVIDENDS_XPATH)
        dividend = "--"
        if len(parsed_output) > 0:
            dividend = parsed_output[0]
        result["dividend"] = dividend
        
        parsed_output = base_response.xpath(ReutersLibrary.DESCRIPTION_XPATH)
        if len(parsed_output) > 0:
            result["description"] = parsed_output[0]
        
        return result
    
    @staticmethod
    def get_NZX_50():
        response = ReutersLibrary.get_response("", ReutersLibrary.NZX50_URL)
        return response.xpath(ReutersLibrary.NZX50_XPATH)
    
    @staticmethod
    def get_NZX():
        response = ReutersLibrary.get_response("", ReutersLibrary.NZX_URL)
        stocks = response.xpath(ReutersLibrary.NZX_XPATH)
        stocks_with_nz = []
        for stock in stocks:
            stocks_with_nz.append(stock + ".NZ")
        return stocks_with_nz
