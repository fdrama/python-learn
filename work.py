# coding:utf-8
import json

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':

    base_url = 'http://www.luxunmuseum.com.cn/cx/'
    response = requests.get(base_url + 'works.php')
    soup = BeautifulSoup(response.text, 'html.parser')

    menu_box = soup.find("div", class_="Menubox")
    content_box = soup.find("div", class_="Contentbox")

    # 查询所有菜单项
    lis = menu_box.find_all('li')
    menu_dict = {}
    for li in lis:
        # 根据菜单项id 去内容div 查询著作链接
        lid = li['id']
        div_id = 'con_one_' + lid[len(lid) - 1]
        div = content_box.find('div', id=div_id)
        links = div.find_all('a')
        link_detail_list = []
        for link in links:
            link_detail = {link.text: link['href']}
            link_detail_list.append(link_detail)
        menu_dict[li.text] = link_detail_list

    with open('menu_dict.json', 'w', encoding='utf-8') as w:
        w.write(json.dumps(menu_dict, indent=4, ensure_ascii=False))

    menu_doc = {}
    for k, v in menu_dict.items():
        if not isinstance(v, list):
            break
        print(k)
        doc_list = []
        for doc in v:
            if not isinstance(doc, dict):
                break
            doc_dict = {}
            for name, extra_url in doc.items():
                print(name)
                response = requests.get(base_url + extra_url)
                soup2 = BeautifulSoup(response.text, 'html.parser')
                div = soup2.find('div', class_='for3_table')
                table = div.find('table')
                # 选择 thead
                thead = table.find('thead')
                # 选择 th
                ths = thead.find_all('th')

                # 选择 tbody
                tbody = table.find('tbody')
                # 选择 tr
                trs = tbody.find_all('tr')
                # 遍历 tr
                articles = []
                for index, th in enumerate(ths):
                    # 选择 td
                    tr = trs[index]
                    tds = tr.find_all('td')
                    attr = {}
                    for td in tds:
                        data_tabel = td['data-tabel']
                        if th.text == '内容':
                            a = td.find('a')
                            attr[th.text] = a['href']
                        else:
                            attr[data_tabel] = th.text
                    articles.append(attr)
                doc_dict[name] = articles
            doc_list.append(doc_dict)

            with open('doc.json', 'w', encoding='utf-8') as w:
                w.write(json.dumps(doc_list, indent=4, ensure_ascii=False))
        menu_doc[k] = doc_list
        with open('menu_doc.json', 'w', encoding='utf-8') as w:
            w.write(json.dumps(menu_doc, indent=4, ensure_ascii=False))
        break
