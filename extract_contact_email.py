import requests
from bs4 import BeautifulSoup
import re
import sys
import csv

# plan
# open html
# find contact us page
# load contact us page
# search for an email in the page
csv_headers = ['Website', 'Contact_mail']
csv_filename = "output.csv"
csv_file = open(csv_filename, 'w')
csvwriter = csv.writer(csv_file)
csvwriter.writerow(csv_headers)
def is_relative(string: str) -> str:
    print(string)
    if(string.startswith('/')):
        print("its relative")
        return 'True'
    elif(string.startswith('#')):
        return 'continue'

    print("its not")
    return 'False'
try:
    website_list = sys.argv[1]
except IndexError:
    print("pass website_list.txt argument")
    sys.exit()
with open(website_list) as addresses:
    for address in addresses:
        print(address.strip())
        home_page = 'http://' + address.strip()
        source = requests.get(home_page).text
        html = BeautifulSoup(source, 'html5lib')
        for anchor in html.find_all("a", href=True):
            if(anchor.text.lower() == 'contact' or anchor.text.lower() == 'contact us'):
                # print(anchor['href'])
                if (is_relative(anchor['href']) == 'True'):
                    contact_url = home_page + anchor['href']
                    print(contact_url)
                elif(is_relative(anchor['href']) == 'continue'):
                    continue
                else:
                    contact_url = anchor['href']
                    print(contact_url)
                contact = requests.get(contact_url).text
                contact_page = BeautifulSoup(contact, 'html5lib')
                for link in contact_page.findAll('a', attrs={'href': re.compile("^mailto:")}):
                    print(link["href"].split(':')[1])
                    csvwriter.writerow([home_page, link["href"].split(':')[1]])

csv_file.close()