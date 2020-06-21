import re
import csv
from requests_html import HTMLSession


base_url = "https://www.lateinamerikaverein.de/de/ueber-uns/mitglieder/p/"
with open(f'all-members.csv', 'w', newline='') as csv_file:
    fieldnames = ["name", "address", "web", "email", "tel",]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(20):
        session = HTMLSession()
        url = f"{base_url}{i}/"
        webpage = session.get(url)
        webpage.html.render()
        results = webpage.html.find("#members-search-results", first=True)
        members = results.find(".accordion__content")
        print(len(members))
        for member in members:
            links = member.find(".memberBody > .row > .column a")
            details = member.find(".memberBody > .row > .column", first=True).text.split("\n")
            adress = details[:3]
            member_name = member.find(".memberHeader")[0].text
            tel_tag = member.find("p", containing="Tel:", first=True)
            if tel_tag is not None:
                phone = re.findall(r'\d+', tel_tag.html)
                tel = ''.join(phone)
            if links is None:
                web = "none"
            elif links == []:
                web = "none"
            elif isinstance(links, list):
                print(links)
                web = links[0].attrs['href']
            else:
                web = links.attrs['href']
            member_dict = {
                "name": member_name,
                "address": member.find(".memberBody > .row > .column p")[0].text.replace("\n", " "),
                "web": web,
                "email": links[1].attrs['href'].replace("mailto:", "") if len(links) == 2 else "None",
                "tel": tel if tel_tag is not None else "None"
            }
            writer.writerow(member_dict)