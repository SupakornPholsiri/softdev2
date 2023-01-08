from requests_html import HTMLSession
from bs4 import BeautifulSoup
s = HTMLSession()
response = s.get("https://www.thairath.co.th")
response.html.render()

soup = BeautifulSoup(response.text, 'html.parser')
for i in soup.find_all(id = "TR_Navbar_Hamburger_Facebook"):
    print(i.prettify(), end = "\n---------------------------------\n")
#print(soup.prettify())