import requests
import phonenumbers
from bs4 import BeautifulSoup
import re
import html
from urllib.parse import urlparse
import validators
from urllib.parse import urlparse


def get_domain(url):
    # Parse the URL

    parsed_url = urlparse(url)

    # Extract the domain (hostname) from the parsed URL
    domain = parsed_url.netloc

    # remove the 'www.' prefix, you can do that as well
    if domain.startswith("www."):
        domain = domain[4:]

    return domain.split(".")[0]


def get_image_name(image_path):
    rez = str(image_path).split('.')
    if len(rez) > 1:
        rez = rez[-2]
    else:
        rez = ''

    return rez.split('/')[-1]


def normalize_url(url):
    # Define a regex pattern to match and remove "www" subdomains
    www_pattern = r'^https?://(?:www\.)?'

    # Apply the regex pattern to both URLs
    normalized = None
    if re.sub(www_pattern, '', url):
        normalized = re.sub(www_pattern, '', url)
    else:
        normalized = None
    return normalized


def find_text_window(html, string):
    ind = html.text.find(string)
    return html.text[(ind - 100): (ind + 100)]


def clean_phone_string(numbers):
    new_list = []
    # Use a regular expression to replace non-digit, +, (, ), or space characters with spaces
    for string in numbers:
        cleaned_string = re.sub(r'[^0-9+() ]', ' ', string)
        new_list.append(cleaned_string)

    return new_list


def create_set_of_numbers(numbers):
    '''
    Function takes list of phone numbers as input argument and created dictionary in a form
     {phone_number: phone_number_only_digits}.
    New dictionary is created - the value for previous dic will be append only if it is the first occurance of a value
    Then, set is created out of keys from the second_dictionary
    :param numbers: list of strings
    :return: set of unique strings
    '''

    digits = dict()
    for number in numbers:
        digits_only = re.sub(r'\D', '', number)
        digits[number] = digits_only

    # Create a new dictionary to store the first occurrences of values
    first_occurrence_dict = {}
    for key, value in digits.items():
        if value not in first_occurrence_dict.values():
            first_occurrence_dict[key] = value

    return list(first_occurrence_dict.keys())


def get_html(url):
    headers = {
        'User-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
    }

    html = requests.get(url, headers=headers)
    return html


def find_regex_inside_p(html):
    phone_regex = r'[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\d]*\d'
    text = html.text.replace('&a;', '&').replace('&q;', '"').replace('&s;', '\\').replace('&l;', '<').replace('&g;',
                                                                                                              '>')
    soup = BeautifulSoup(text, "html.parser")  # generate beautifulSoup object

    numbers = []
    for tag in soup.find_all('p'):
        # print (tag)
        matches = re.findall(phone_regex, str(tag))
        if matches:
            numbers.extend(matches)

    filtered_strings = [string for string in numbers if 6 <= sum(c.isdigit() for c in string) <= 15]

    set_of_numbers = set(filtered_strings)
    return set_of_numbers


def remove_scripts_and_onclicks_from_html(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    # Find all elements with the onclick attribute and remove it
    for element in soup.find_all(attrs={"onclick": True}):
        del element['onclick']

    # Get the modified HTML
    modified_html = str(soup)
    return modified_html

def find_regex_inside_html(html):
    phone_regex = r'[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\d]*\d'
    matches = re.findall(phone_regex, str(html.text))

    # for number in filtered_strings:
    novo = []
    for number in matches:
        try:
            z = phonenumbers.parse(number, None)
            if phonenumbers.is_possible_number(z):
                novo.append(number)
        except:
            continue
    return novo


def try_random_regex(html):
    regex = r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
    matches = re.findall(regex, str(html.text))
    filtered_strings = [string for string in matches if 6 <= sum(c.isdigit() for c in string) <= 15]
    set_of_numbers = set(filtered_strings)
    return set_of_numbers
