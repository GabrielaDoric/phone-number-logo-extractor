import re
import utils
from extractors.extractor import Extractor


class Extractor_Phone(Extractor):

    def __init__(self, html):
        self.html = html

    def extract(self):
        phone_numbers = self._key_words_around_number()
        if not phone_numbers:
            phone_numbers = None

        return phone_numbers

    def _key_words_around_number(self):
        '''
        This function serves the following purposes:
        Utilizing a general phone number regular expression, it identifies potential phone numbers within a given text and
        captures the surrounding text substrings.
        It then iterates over a dictionary, associating each potential phone number with its respective text window.
        Within each text window, it searches for specific keywords that strongly suggest the potential phone number is indeed
        a valid phone number.
        If the predefined criteria are met, the function adds the validated phone number to a list.
        Finally, it returns a set containing the verified phone numbers extracted from the list.
        :param html: requests.Response Object
        :return: string
        '''

        base_phone_regex = r'[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\d]*\d'  # general_phone_regex
        matches = re.findall(base_phone_regex, self.html.text)  # str(unescape(html.text)))

        matches = [string for string in matches if 6 <= sum(c.isdigit() for c in string) <= 15]
        # matches = [string for string in matches if len(string)>=7]  # da maknem smeća iz htmla

        key_words = ['tel:', 'phone', 'Number', 'Tel:', 'Fax', 'customer-support', 'contact', 'Customer Service',
                     'Contact']

        dict_of_matches = dict()
        phone_numbers = []
        for match in matches:
            pattern = r'\(\d{3}\) \d{3}-\d{4}'  # search for standard formats: e.g. (517) 788-0550
            if re.findall(pattern, match):
                phone_numbers.append(match)
                continue

            dict_of_matches[match] = utils.find_text_window(self.html, match)

        for key, value in dict_of_matches.items():
            for distinct_word in key_words:
                if distinct_word in value:
                    phone_numbers.append(key)

        selected_numbers = utils.create_set_of_numbers(phone_numbers)
        return ", ".join(selected_numbers)


def main():
    with open('../companies.txt') as f:
        urls = [line.rstrip() for line in f if line.strip() != '']

    for url in urls:
        html = utils.get_html(url.rstrip('/'))

        extractor_phone = Extractor_Phone(html)
        phone_numbers = extractor_phone.extract()

        print(url + ' >> ' + str(phone_numbers))


if __name__ == '__main__':
    main()
