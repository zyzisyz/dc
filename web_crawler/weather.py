

from html.parser import HTMLParser
from urllib import request
import pickle
import json


class WeatherHtmlParser(HTMLParser):
    def __init__(self):
        self.flag = False
        self.weather_data = None
        super(WeatherHtmlParser, self).__init__()

    def handle_starttag(self, tag, attr):
        if tag == "script":
            self.flag = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.flag = False

    def handle_data(self, data):
        if self.flag:
            if "var hour3data=" in data:
                data = data.strip("\n")
                data = data.strip("var hour3data=")
                self.weather_data = json.loads(data)


class CityCodeHtmlParser(HTMLParser):

    def __init__(self):
        self.flag = False
        self.city_dict = {}
        super(CityCodeHtmlParser, self).__init__()

    def handle_starttag(self, tag, attr):
        if tag == "p" or tag == "br":
            self.flag = True

    def handle_endtag(self, tag):
        if tag == "p" or tag == "br":
            self.flag = False

    def handle_data(self, data):
        if self.flag:
            if "=" in data:
                data = data.split("=")
                self.city_dict[data[1]] = data[0]


def printWeatherInfo(func):
    def call():
        info = func()
        if info == None:
            return None

        # 一天之内的天气
        one_day = info["1d"]
        for item in one_day:
            item = item.split(",")
            print("%s::天气：%s； 温度：%s； 风向：%s； 风力：%s" %
                  (item[0], item[2], item[3], item[4], item[5]))

        # 未来7天内的天气
        flag = input("是否打印未来7天内的天气：")
        if flag == "是":
            seven_day = info["7d"]
            for i in range(7):
                if i >= 1:
                    for item in seven_day[i]:
                        item = item.split(",")
                        print("%s::天气：%s； 温度：%s； 风向：%s； 风力：%s" %
                              (item[0], item[2], item[3], item[4], item[5]))
        else:
            return None

    return call


# 抓取天气信息
@printWeatherInfo
def getAllWeather():
    city = input("请输入你要查询的城市：")
    city = queryCityCode(city)
    if city == None:
        return None
    url_address = "http://www.weather.com.cn/weather1d/%s.shtml" % city
    req = request.Request(url_address)
    req.add_header(
        "User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36")
    with request.urlopen(req) as html:
        data = html.read().decode("utf-8")
        html_parser = WeatherHtmlParser()
        html_parser.feed(data)
        html_parser.close()
        return html_parser.weather_data


def queryCityCode(city_name):
    def getAllCityInfo():
        url_address = "http://doc.orz520.com/a/doc/2014/0322/2100581.html"
        req = request.Request(url_address)
        req.add_header(
            "User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36")
        with request.urlopen(req) as html:
            data = html.read().decode("utf-8")
            html_parser = CityCodeHtmlParser()
            html_parser.feed(data)
            html_parser.close()
            return html_parser.city_dict

    city_dict = getAllCityInfo()
    if city_name not in city_dict:
        return None
    return city_dict[city_name]


if __name__ == "__main__":
    getAllWeather()
