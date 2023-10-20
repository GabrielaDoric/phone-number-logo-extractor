import re
import requests
from bs4 import BeautifulSoup
import utils
from html import unescape
from lxml.html.clean import clean_html
import phonenumbers


def key_words_around_number(html):
    '''
    Find potential phone numbers in the given text using regex.
    For each found potential number, extract a text window around it.
    Check if the number has a standard format like (800) 433-2652;
    if so, add it to the list of found numbers.
    If the format is not standard, create a dictionary where the potential
    number is the key and the text window is the value.
    Iterate through the dictionary and identify if the text window contains
    keywords like 'tel:', 'phone', 'contact us', etc., and add them to
    the list of found phone numbers.

    Returns a set of unique found phone numbers.

    :param html: html reponse
    :return: set of found phone numbers
    '''

    base_phone_regex = r'[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\d]*\d'  # general_phone_regex
    matches = re.findall(base_phone_regex, html.text)  # str(unescape(html.text)))

    matches = [string for string in matches if 6 <= sum(c.isdigit() for c in string) <= 15]
    # matches = [string for string in matches if len(string)>=7]  # da maknem smeća iz htmla
    dict_of_matches = dict()
    key_words = ['tel:', 'phone', 'Number', 'Tel:', 'Fax', 'customer-support', 'contact', 'Customer Service',
                 'Contact']

    phone_numbers = []
    for match in matches:
        pattern = r'\(\d{3}\) \d{3}-\d{4}'  # search for standard formats: e.g. (517) 788-0550
        if re.findall(pattern, match):
            phone_numbers.append(match)
            continue

        dict_of_matches[match] = utils.find_text_window(html, match)

    for key, value in dict_of_matches.items():
        for distinct_word in key_words:
            if distinct_word in value:
                phone_numbers.append(key)

    selected_numbers = utils.create_set_of_numbers(phone_numbers)
    return selected_numbers


if __name__ == '__main__':

    with open('companies.txt') as f:
        urls = [line.rstrip() for line in f if line.strip() != '']

    for url in urls:
        url = url.strip('/')
        html = utils.get_html(url)  # retrieve html

        # print ('Company: ' + url + ' Phone numbers: ' + str(utils.find_regex_inside_p(html)))
        # print('Company: ' + url + ' Phone numbers: ' + str(utils.find_regex_inside_html(html)))
        # print('Company: ' + url + ' Phone numbers: ' + str(utils.try_random_regex(html)))

        print('Company: ' + url + 'Phone: ', key_words_around_number(html))
