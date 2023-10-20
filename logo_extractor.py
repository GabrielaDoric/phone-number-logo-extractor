from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from html import unescape
import utils
import urllib.parse
from requests.utils import requote_uri

def find_logo_with_keywords(html, url):
    '''
    Iterate through the images in the HTML.
    Check if the image name contains both the word 'logo' and a word extracted from the argument URL.
    If so, consider it a logo image and append it to a list.
    Among the picked images, prioritize images that contain the word 'color' in their name.
    If no such 'color' image is found, return the first image in the list.
    :param html: requests.Response Object
    :param url: string
    :return: string
    '''
    logos = []
    final_logo = None
    company_name = utils.extract_domain_from_url(url)

    soup = BeautifulSoup(html.text, 'html.parser')
    img_tags = soup.findAll('img', {"src": True})
    for img_tag in img_tags:
        img_name = utils.get_image_name(img_tag['src'])
        if img_name == '':
            continue

        if 'logo' in img_name.lower() and company_name.lower() in img_name.lower():
            absolute_path = urllib.parse.urljoin(url, img_tag['src'])
            logos.append(absolute_path)

        if not logos:
            final_logo = None
        else:
            final_logo = logos[0]
            for logo in logos:
                if 'color' in str(logo) or 'colour' in str(logo):
                    final_logo = logo

    return final_logo


def find_logo_with_self_reference(html, url):
    '''
    The function searches for HTML 'a' elements that contain 'href' attributes.
    It iterates through each found element to determine if the 'href' attribute is self-referential.
    If a self-referential 'href' attribute is found, the function saves the link to the image and returns it.
    :param html: requests.Response Object
    :param url: string
    :return: string
    '''
    absolute_urls = []
    solution = None
    soup = BeautifulSoup(html.text, 'html.parser')
    a_elements = soup.find_all('a', {"href": True})
    for a_element in a_elements:
        if a_element['href'] == "/" or utils.normalize_url(str(a_element['href']).strip('/')) == utils.normalize_url(
                str(url)):  # if or a_element['href'] == "/":
            pattern = r'src="([^"]+)"'
            matches = re.findall(pattern, str(a_element))

            # if url is not absolute, add base url to it
            absolute_urls = [urljoin(url, match) for match in matches]  # create absolute path
            absolute_urls = [unescape(i) for i in absolute_urls]  # remove special charachters like &alt

            if matches:
                break

    if absolute_urls:
        solution = absolute_urls[0]

    return solution


def find_first_occurred_logo(html, url):
    '''
    This method ensures that images with 'logo' in their names are considered, with a preference given to those
    containing the word 'color' when available. If no such images exist, the first image is chosen.
    :param html: requests.Response Object
    :param url: string
    :return: string
    '''

    soup = BeautifulSoup(html.text, 'html.parser')
    img_tags = soup.findAll('img', {"src": True})
    found_logos = []
    #encoded_url = None
    for img_tag in img_tags:
        if 'logo' in str(img_tag).lower():
            absolute_path = urllib.parse.urljoin(url, img_tag['src'])
            # print(absolute_path)
            encoded_url = requote_uri(absolute_path)
            found_logos.append(encoded_url)

    if not found_logos:
        final_logo = None
    else:
        final_logo = found_logos[0]
        for logo in found_logos:
            if 'color' in str(logo) or 'colour' in str(logo):
                final_logo = logo

    return final_logo


if __name__ == '__main__':

    with open('companies.txt') as f:
        urls = [line.rstrip() for line in f if line.strip() != '']

    for url in urls:
        # for url in [urls[5]]:
        #url = url.strip('/')
        html = utils.get_html(url.strip('/'))  # retrieve html
        logo_found = False

        img_logo = find_logo_with_keywords(html, url)
        if img_logo is not None:
            logo_found = True
        if not logo_found:
            img_logo = find_logo_with_self_reference(html, url)
        if img_logo is not None:
            logo_found = True
        if not logo_found:
            img_logo = find_first_occurred_logo(html, url)

        print(url + '>>' + str(img_logo))

