import requests
from urllib.parse import urlparse
import re


def get_domain(url):
    """
    Extracts the primary domain name from a URL, excluding any 'www' prefix.

    Args:
        url (str): The URL from which the domain name should be extracted.

    Returns:
        str: The primary domain name, excluding the 'www' prefix if present.
    """
    # Parse the URL

    parsed_url = urlparse(url)

    # Extract the domain (hostname) from the parsed URL
    domain = parsed_url.netloc

    # remove the 'www.' prefix, you can do that as well
    if domain.startswith("www."):
        domain = domain[4:]

    return domain.split(".")[0]


def get_image_name(image_path):
    """
    Extracts the name of an image file from its path.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The name of the image file without the file extension and any directory path.
    """
    rez = str(image_path).split('.')
    if len(rez) > 1:
        rez = rez[-2]
    else:
        rez = ''

    return rez.split('/')[-1]


def normalize_url(url):
    """
    Removes "www" subdomains from a URL, providing a normalized version.

    Args:
        url (str): The URL to be normalized.

    Returns:
        str: The URL with "www" subdomains removed or None if no change is needed.
    """
    # Define a regex pattern to match and remove "www" subdomains
    www_pattern = r'^https?://(?:www\.)?'

    if re.sub(www_pattern, '', url):
        normalized = re.sub(www_pattern, '', url)
    else:
        normalized = None
    return normalized


def find_text_window(html, string):
    """
    Locates a specific string within an HTML document and returns a text window of 100 characters around the match.

    Args:
        html (str): Response Object
        string (str): The target string to search for within the HTML document.

    Returns:
        str: A 100-character window of text around the first occurrence of the target string.
    """
    ind = html.text.find(string)
    return html.text[(ind - 100): (ind + 100)]


def create_set_of_numbers(numbers):
    """
    Extracts unique numbers from a list, keeping the first occurrence of each value.

    Args:
        numbers (list): A list of strings containing numbers.

    Returns:
        list: A list of numbers with only the first occurrence of each value.
    """
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
    """
    Fetches the HTML content of a web page from the specified URL.

    Args:
        url (str): The URL of the web page to retrieve HTML from.

    Returns:
        str: The HTML content of the web page.
    """
    headers = {
        'User-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
    }

    html = requests.get(url, headers=headers)
    return html
