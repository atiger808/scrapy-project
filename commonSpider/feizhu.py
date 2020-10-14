import requests
from getheaders import getheaders
url = 'https://hotel.fliggy.com/hotel_detail2.htm?shid=52230531&city=330100&checkIn=2020-06-24&checkOut=2020-06-25&hotelType=kezhan&_output_charset=utf8'

heades = getheaders()
res = requests.get(url, headers=heades)
print(res.text)