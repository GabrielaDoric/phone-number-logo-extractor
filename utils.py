import requests
from urllib.parse import urlparse
import re


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
