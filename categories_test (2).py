import pytest
import requests
import dicttoxml
import xmltodict

categories_url = 'http://164.92.218.36:8080/api/categories'
auth = ('1VQDHXQ8EF73QTHESPT7UHU9AJQPLXXL', '')

def test_get_categories():
    response = requests.get(categories_url, auth=auth)

    assert response.status_code == 200

    print(response)

payload = '''<?xml version="1.0" encoding="UTF-8"?>
    <prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
        <category>
            <id_parent></id_parent>
            <active>0</active>
            <id_shop_default></id_shop_default>
            <is_root_category>0</is_root_category>
            <position></position>
            <date_add></date_add>
            <date_upd></date_upd>
            <name><language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1">new name</language></name>
            <link_rewrite>
                <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1"></language>
            </link_rewrite>
            <description>
                <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1"></language>
            </description>
            <meta_title>
                <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1"></language>
            </meta_title>
            <meta_description>
                <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1"></language>
            </meta_description>
            <meta_keywords>
                <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1"></language>
            </meta_keywords>
            <associations>
                <categories nodeType="category" api="categories"/>
                <products nodeType="product" api="products"/>
            </associations>
        </category>
    </prestashop>'''

def test_create_category():
    
    headers = {"Content-Type": "application/xml"}
    response = requests.post(categories_url, headers=headers, auth=auth, data=payload)

    assert response.status_code == 201
    resultCategories = xmltodict.parse(response.content)['prestashop']['category']
    

    assert resultCategories ['name']['language']['#text'] == 'new name'
    id = resultCategories ['id']

    response = requests.get(categories_url + '/' + id, auth=auth)

    assert response.status_code == 200
    resultCategories  = xmltodict.parse(response.content)['prestashop']['category']

    assert resultCategories['name']['language']['#text'] == 'new name'
    assert resultCategories ['id'] == id

   
    
def test_put_category_405_not_enough_permissions():
    headers = {"Content-Type": "application/xml","Accept": "application/xml"}
    response = requests.put(categories_url, headers=headers, auth=auth, data=payload)

    assert response.status_code == 405
    


    
def test_delete_category_405_not_enough_permissions():
    headers = {"Content-Type": "application/xml","Accept": "application/xml"}
    response = requests.put(categories_url, headers=headers, auth=auth, data=payload)

    assert response.status_code == 405
    




    
