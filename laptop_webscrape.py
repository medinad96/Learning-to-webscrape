import bs4, re
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 

my_url1 = 'https://www.newegg.com/Laptops-Notebooks/Category/ID-223?Tpk=laptops' #'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics%20cards'

filename = "products2.csv"

f = open(filename, "w")


def webScrape(my_url):
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close() 

	# html parsing
	page_soup = soup(page_html,"html.parser")
	# each product
	containers = page_soup.findAll("div",{"class":"item-container"})

	

	headers = "brand, product_name, price, shipping \n"

	f.write(headers)
	 
	for container in containers:
		
		
			 #container.findAll("a",{"class":"item-branding"})
		#brand = "brand" #brand_container.img["title"]
		
		title_container = container.findAll("a",{"class":"item-title"})
		brand = title_container[0].text.partition(" ")[0]
		product_name = title_container[0].text
		price_container = container.findAll("li",{"class":"price-current"})
		price_temp = price_container[0].text
		decimal = re.compile(r'\d+\.\d+') 
		price = [float(i) for i in decimal.findall(price_temp)]
		price = "$"+str(price[0])

		shipping_container = container.findAll("li",{"class":"price-ship"})
		shipping = shipping_container[0].text.strip()

		print("brand: " + brand)
		print("product_name: " + product_name)
		print("price:" + price)
		print("shipping: " + shipping)

		f.write(brand +","+ product_name.replace(",","|") +","+ price.replace("(","") +","+ shipping + "\n")


count = 0 
#I is the number of pages from the site
for i in range(3):
	url2 = 'https://www.newegg.com/Laptops-Notebooks/SubCategory/ID-32/Page-={}?Tid=6740&PageSize=36&order=BESTMATCH'.format(i)
	webScrape(url2)
f.close()
#print("PAGES Crawled"+count)