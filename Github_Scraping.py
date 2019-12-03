from bs4 import BeautifulSoup
import requests
import csv

# CSV file details
CSV_FILE_NAME = "results.csv"
CSV_FILE_COLUMNS = ['Name', 'Link', 'Short Description', 'Programming Language', 'List of tags']


# a function to check if the input is none or not
def check_none(obj):
    if obj is not None:
        return True
    else:
        return False


# preparing the csv file
# I am using (w+) parameter in order to clear the file before writing to it
csv_file = open(CSV_FILE_NAME, "w+", encoding="utf-8", newline='')
csv_writer = csv.writer(csv_file)

# Writing titles row
csv_writer.writerow(CSV_FILE_COLUMNS)

# initialize for the first page
page_index = 1
url = "https://github.com/github?page={}".format(page_index)
source = requests.get(url).text
soup = BeautifulSoup(source, 'lxml')
# check if page exists
check = check_none(soup.find("h3", string="This organization has no more repositories."))
# scraping all the pages until we reach the end
while not check:
    # navigate to the list items were the required information is stored
    repo_list = soup.find("div", {"class": "org-repos repo-list"}).find('ul').findAll("li")
    for li in repo_list:
        # finding the link and the name of the repo
        a = li.find("a", {"class": "d-inline-block"})
        link = 'https://github.com' + a['href']
        name = a.text.strip()
        # finding the description
        p = li.find("p", {"itemprop": "description"})
        # some repos does not have short description
        if check_none(p):
            short_description = p.text.strip()
        else:
            short_description = "No short description given"

        # finding tags
        tags = li.findAll("a", {"class": "topic-tag topic-tag-link f6 my-1"})
        tags_list = list()
        for tag in tags:
            tags_list.append(tag.text.strip("\n").strip())

        # converting the list to text in order to add it to the csv file
        if tags_list == list():
            tags_text = "No tags provided"
        else:
            tags_text = ", ".join(tags_list)

        # finding the programming language used
        span = li.find("span", {"itemprop": "programmingLanguage"})
        # some repos does not indicate the used programming language
        if check_none(span):
            programming_language = span.text.strip()
        else:
            programming_language = "Not given"
        # Writing data to the csv file
        row = [name, link, short_description, programming_language, tags_text]
        csv_writer.writerow(row)
    # moving to next page
    page_index += 1
    url = "https://github.com/github?page={}".format(page_index)
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    # checking if it exists
    check = check_none(soup.find("h3", string="This organization has no more repositories."))

csv_file.close()
