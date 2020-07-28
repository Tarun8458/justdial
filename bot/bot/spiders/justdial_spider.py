import scrapy
from ..items import BotItem
from bs4 import BeautifulSoup


phoneNumberMap = {
        "icon-fe" : "(",
        "icon-dc" : "+",
        "icon-hg" : ")",
        "icon-ba" : "-",
        "icon-acb" : "0",
        "icon-yz" : "1",
        "icon-wx" : "2",
        "icon-vu" : "3",
        "icon-ts" : "4",
        "icon-rq" : "5",
        "icon-po" : "6",
        "icon-nm" : "7",
        "icon-lk" : "8",
        "icon-ji" : "9",
    }

def phoneNumberCreator(bsObject):
    phoneNumber = ""
    for obj in bsObject:
        try:
            phoneNumber += phoneNumberMap[obj.attrs['class'][1]]
        except:
            print("error at object :", obj)
            return "Invalid Phone Number"
    return phoneNumber

class justdialspider(scrapy.Spider):

    name = 'justdial'

    page_number = 2
    start_urls =  [
                      'https://www.justdial.com/Delhi/Estate-Agents-For-Residential-Rental/page-2'
    ]

    def parse(self, response):
         items= BotItem()

         name=response.css('.lng_cont_name::text').extract()
         rating = response.css('.green-box::text').extract()
         phone = response.css('.contact-info').extract()
         address = response.css('.cont_sw_addr::text').extract()
         for index in range(len(address)):
             address[index] = address[index].replace("\n","")
             address[index] = address[index].replace("\t", "")

         phoneNumberList = []

         for index in range(len(phone)):
             soup = BeautifulSoup(phone[index], 'html.parser')
             mobile_data_unparsed = soup.find_all("span", {"class": "mobilesv"})
             phoneNumberList.append(phoneNumberCreator(mobile_data_unparsed))

         items['name'] = name
         items['rating'] = rating
         items['phone'] = phoneNumberList
         items['address'] = address

         yield items

         next_page = 'https://www.justdial.com/Delhi/Estate-Agents-For-Residential-Rental/page-'+str(justdialspider.page_number)
         if justdialspider.page_number <= 10:
             justdialspider.page_number +=1
             yield response.follow(next_page, callback= self.parse)