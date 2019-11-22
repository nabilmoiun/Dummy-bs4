import json
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from elasticsearch import Elasticsearch

elastic_search = Elasticsearch([{'host': 'localhost', 'port': '9200'}])


def get_a_drug_information(drug_page_link):
    drugs_and_information = {}
    request_url = urlopen(drug_page_link).read()
    raw_data = bs(request_url, 'html.parser')
    medicine_name = raw_data.find('h1', class_='page-heading-1-l').span.text
    # print("medicine name : ", medicine_name)
    headers = raw_data.find_all('h4', class_='ac-header')
    # [print(header.text) for header in headers]
    scopes = raw_data.find_all('div', class_='col-xs-12 ac-body')
    # [print(header.text) for header in scopes]
    for i in range(len(headers)):
        drugs_and_information[headers[i].text] = scopes[i].text
    print(drugs_and_information)
    return medicine_name, drugs_and_information


def dump_into_elasticsearch(dictionary, id):
    elastic_search.index(index='medex_drugs', ignore=400, id=id, body=dictionary)


key = '1stCef Capsule'
query = json.dumps(
    {
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": "chemotherapies",
                            # "type": "cross_fields",
                            "fields": ["Overdose Effects"]
                            # "minimum_should_match": "50%"
                        }
                    },
                    {
                        "multi_match": {
                            "query": "Fluorouracil",
                            # "type": "cross_fields",
                            "fields": ["Indications"]
                        }
                    },
{
                        "multi_match": {
                            "query": "cancer",
                            # "type": "cross_fields",
                            "fields": ["Pharmacology"]
                        }
                    }
                ]
            }
        }
    }
    )
result = elastic_search.search(index='medex_drugs', ignore=400, body=query)
document = elastic_search.get(index='medex_drugs', id=key)
print(document)
content = document['_source']
for k, v in content.items():
    print(k, v)
# print(result)
from_page = 1
to_page = 2
medex_home_url = 'https://medex.com.bd/brands?page='

# for page in range(from_page, to_page):
#     print("page : ", page)
#     link_url = medex_home_url + str(page)
#     link_url_open = urlopen(link_url).read()
#     raw_links = bs(link_url_open, 'html.parser')
#     links = raw_links.find_all('a', class_='hoverable-block')
#     id = 1
#     for link in links:
#         id += 1
#         content = get_a_drug_information(link.get('href'))
#         dump_into_elasticsearch(content[1], "{id}".format(id=content[0]))

