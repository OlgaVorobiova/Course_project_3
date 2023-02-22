import pytest
import requests
import dicttoxml
import xmltodict

addresses_url = 'http://164.92.218.36:8080/api/addresses'
auth = ('1VQDHXQ8EF73QTHESPT7UHU9AJQPLXXL', '')

address = {
    "address": {
        "id_customer": "",
        "id_manufacturer": "",
        "id_supplier": "",
        "id_warehouse": "",
        "id_country": 1,
        "id_state": "",
        "alias": "artem",
        "company": "",
        "lastname": "Vorobiova",
        "firstname": "Olha",
        "vat_number": "",
        "address1": "Illinska street 184",
        "address2": "",
        "postcode": "",
        "city": "Charkiv",
        "other": "",
        "phone": "",
        "phone_mobile": "",
        "dni": ""
    }
}


def test_create_and_delete_address():
    #given
    xml = dicttoxml.dicttoxml(
        address, custom_root='prestashop', attr_type=False)
    
    #when create

    response = requests.post(addresses_url, data=xml, auth=auth)

    #then

    assert response.status_code == 201
    resultAddress = xmltodict.parse(response.content)['prestashop']['address']

    assert resultAddress['lastname'] == address['address']['lastname']
    id = resultAddress['id']

    response = requests.get(addresses_url + '/' + id, auth=auth)

    assert response.status_code == 200
    resultAddress = xmltodict.parse(response.content)['prestashop']['address']

    assert resultAddress['lastname'] == address['address']['lastname']
    assert resultAddress['id'] == id

    #when delete

    response = requests.delete(addresses_url + '/' + id, auth=auth)

    #then

    assert response.status_code == 200

    response = requests.get(addresses_url + '/' + id, auth=auth)

    assert response.status_code == 404

address_for_update = {
    "address": {
        "id":"",
        "id_customer": "",
        "id_manufacturer": "",
        "id_supplier": "",
        "id_warehouse": "",
        "id_country": 1,
        "id_state": "",
        "alias": "artem",
        "company": "",
        "lastname": "Vorobiova",
        "firstname": "Olha",
        "vat_number": "",
        "address1": "Illinska street 184",
        "address2": "",
        "postcode": "",
        "city": "Charkiv",
        "other": "",
        "phone": "",
        "phone_mobile": "",
        "dni": ""
    }
}

def test_update_address():
    #given address exists
    xml = dicttoxml.dicttoxml(
        address, custom_root='prestashop', attr_type=False)

    response = requests.post(addresses_url, data=xml, auth=auth) 
    resultAddress = xmltodict.parse(response.content)['prestashop']
    assert resultAddress['address']['firstname'] == "Olha"
    id = resultAddress['address']['id']
    address_for_update['address']['id'] = id
    address_for_update['address']['firstname'] = 'new name'

    #when address updated

    xml = dicttoxml.dicttoxml(
    address_for_update, custom_root='prestashop', attr_type=False)
    response = requests.put(addresses_url, auth=auth, data=xml)

    assert response.status_code == 200

    resultAddress = xmltodict.parse(response.content)['prestashop']['address']

    assert resultAddress['firstname'] == 'new name'
    assert resultAddress['id'] == id

    #clear data after test

    response = requests.delete(addresses_url + '/' + id, auth=auth)

def test_get_addresses_response_contains_created_adress():
    #given

    xml = dicttoxml.dicttoxml(
        address, custom_root='prestashop', attr_type=False)

    response = requests.post(addresses_url, data=xml, auth=auth) 
    resultAddress = xmltodict.parse(response.content)['prestashop']
    id = resultAddress['address']['id']

    #when

    response = requests.get(addresses_url, auth=auth)

    #then

    assert response.status_code == 200

    address_found = False
    for add in xmltodict.parse(response.content)['prestashop']['addresses']['address']:
        if add['@id'] == id:
            address_found = True
            break
    
    assert address_found 

    #clean

    response = requests.delete(addresses_url + '/' + id, auth=auth)





    
