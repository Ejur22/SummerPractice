import json
import requests
from bs4 import BeautifulSoup


#title = input()
#page = int(input())
def get_vacancies(title, page):
    url = "https://hh.ru/search/vacancy"
    params = {
        "text": title,
        "area": 113,
        "per_page": 100,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "   
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36",
    }

    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find_all('span', class_='vacancy-name--c1Lay3KouCl7XasYakLk serp-item__title-link')
    work_exp = soup.find_all('span', attrs={
        'class': 'label--rWRLMsbliNlu_OMkM_D3 label_light-gray--naceJW1Byb6XTGCkZtUM',
        'data-qa': 'vacancy-serp__vacancy-work-experience'
    })
    salary = soup.find_all('span', class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni '
                                          'compensation-text--kTJ0_rp54B2vNeZ3CTt2 '
                                          'separate-line-on-xs--mtby5gO4J0ixtqzW38wh')
    city = soup.find_all('span', attrs={
        'class': 'bloko-text',
        'data-qa': 'vacancy-serp__vacancy-address'
    })
    #subway = soup.find_all('span', class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni')
    company = soup.find_all('span', class_='company-info-text--vgvZouLtf8jwBmaD1xgp')
    def not_feedback(href):
        if href != 'https://feedback.hh.ru/knowledge-base/article/5951' and href != 'https://feedback.hh.ru/article/details/id/5951':
            return href


    link = soup.find_all('a', attrs={
        'class': 'bloko-link',
        'target': '_blank'
    }, href=not_feedback)

    array = []
    for p in range(0, page):
        data = {
            'title': title[p].text.replace(" ", "").replace(' ', "").replace("\u2009", "").replace("\xa0", " ").replace('0xc2', ''),
            'experience': work_exp[p].text.replace(" ", "").replace(' ', "").replace("\u2009", "").replace("\xa0", " ").replace('0xc2', ''),
            'salary': salary[p].text.replace(" ", "").replace(' ', "").replace("\u2009", "").replace("\xa0", " ").replace('0xc2', ''),
            'city': city[p].text.replace(" ", "").replace(' ', "").replace("\u2009", "").replace("\xa0", " ").replace('0xc2', ''),
            #'subway': subway[p].text.replace(" ", "").replace(' ', "").replace("\u2009", "").replace("\xa0", " ").replace('0xc2', ''),
            'company': company[p].text.replace(" ", " ").replace(' ', " ").replace("\u2009", "").replace("\xa0", " ").replace('0xc2', ''),
            'link': link[p]['href'],
        }
        array.append(data)
    print(array)
    return array

'''
        json_obj = json.dumps(data, indent=3, ensure_ascii=False)

        file_name = './docs/vacancies/{}.json'.format(len(os.listdir('./docs/vacancies')))

        with open(file_name, mode='w', encoding='utf-8') as file:
            file.write(json_obj)
'''

#get_vacancies(title, page)