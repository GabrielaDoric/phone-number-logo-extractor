from bs4 import BeautifulSoup
from urllib.parse import urljoin
from html import unescape
from requests.utils import requote_uri
import urllib.parse
import re
import utils

from extractors.extractor import Extractor


class Extractor_Logo(Extractor):

    def __init__(self, html, url):
        self.html = html
        self.url = url

    def extract(self):
        logo_found = False
        img_logo = self._find_logo_with_keywords()
        if img_logo is not None:
            logo_found = True
        if not logo_found:
            img_logo = self._find_logo_with_self_reference()
        if img_logo is not None:
            logo_found = True
        if not logo_found:
            img_logo = self._find_first_occurred_logo()

        return img_logo

    def _find_logo_with_keywords(self):
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

        resulting_logo = None
        company_name = utils.get_domain(self.url)
        logos = []

        soup = BeautifulSoup(self.html.text, 'html.parser')
        img_tags = soup.findAll('img', {"src": True})
        for img_tag in img_tags:
            img_name = utils.get_image_name(img_tag['src'])
            # if img_name == '':
            #    continue

            if 'logo' in img_name.lower() and company_name.lower() in img_name.lower():
                absolute_path = urllib.parse.urljoin(self.url, img_tag['src'])
                logos.append(absolute_path)

            if not logos:
                resulting_logo = None
            else:
                resulting_logo = logos[0]
                for logo in logos:
                    if 'color' in str(logo) or 'colour' in str(logo):
                        resulting_logo = logo

        return resulting_logo

    def _find_logo_with_self_reference(self):
        '''
        The function searches for HTML 'a' elements that contain 'href' attributes.
        It iterates through each found element to determine if the 'href' attribute is self-referential.
        If a self-referential 'href' attribute is found, the function saves the link to the image and returns it.
        :param html: requests.Response Object
        :param url: string
        :return: string
        '''
        absolute_urls = []
        resulting_logo = None

        soup = BeautifulSoup(self.html.text, 'html.parser')
        a_elements = soup.find_all('a', {"href": True})
        for a_element in a_elements:

            href_url = utils.normalize_url(str(a_element['href']).rstrip('/'))
            base_url = utils.normalize_url(str(self.url).rstrip('/'))
            if a_element['href'] == "/" or href_url == base_url:  # if or a_element['href'] == "/":

                pattern = r'src="([^"]+)"'
                matches = re.findall(pattern, str(a_element))

                absolute_urls = [urljoin(self.url, match) for match in matches]
                absolute_urls = [unescape(i) for i in absolute_urls]  # Remove special characters, e.g. '&alt'

                if matches:
                    break

        if absolute_urls:
            resulting_logo = absolute_urls[0]

        return resulting_logo

    def _find_first_occurred_logo(self):
        '''
        This method ensures that images with 'logo' in their names are considered, with a preference given to those
        containing the word 'color' when available. If no such images exist, the first image is chosen.
        :param html: requests.Response Object
        :param url: string
        :return: string
        '''
        found_logos = []

        soup = BeautifulSoup(self.html.text, 'html.parser')
        img_tags = soup.findAll('img', {"src": True})
        for img_tag in img_tags:
            if 'logo' in str(img_tag).lower():
                absolute_path = urllib.parse.urljoin(self.url, img_tag['src'])
                encoded_url = requote_uri(absolute_path)
                found_logos.append(encoded_url)

        if not found_logos:
            resulting_logo = None
        else:
            resulting_logo = found_logos[0]
            for logo in found_logos:
                if 'color' in str(logo) or 'colour' in str(logo):
                    resulting_logo = logo

        return resulting_logo


def main():
    with open('../companies.txt') as f:
        urls = [line.rstrip() for line in f if line.strip() != '']

    for url in urls:
        # for url in [urls[2]]:
        # url = url.strip('/')
        html = utils.get_html(url.strip('/'))  # retrieve html

        extractor_logo = Extractor_Logo(html, url)
        img_logo = extractor_logo.extract()

        print(url + '>>' + str(img_logo))


if __name__ == '__main__':
    main()
