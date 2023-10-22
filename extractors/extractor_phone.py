import re
import utils
from extractors.extractor import Extractor


class Extractor_Phone(Extractor):

    def __init__(self, html):
        self.html = html

    def extract(self):
        """
        Attempts to extract phone numbers from a web page using a method based on keyword analysis.

        The function searches for phone numbers in the vicinity of specific keywords. If any phone numbers are found, they are returned. If no phone numbers are detected, the function returns None.

        Returns:
            list or None: A list of extracted phone numbers or None if no numbers are found.
        """
        phone_numbers = self._key_words_around_number()
        if not phone_numbers:
            phone_numbers = None

        return phone_numbers

    def _key_words_around_number(self):
        """
        Extracts potential phone numbers from a given text by employing a general phone number regular expression to identify
        and capture numerical sequences. The function then associates each potential phone number with the surrounding text
        context.

        To validate potential phone numbers, it searches for specific keywords that indicate the likelihood of the extracted
        sequence being an actual phone number. If predefined criteria are met, the validated phone numbers are collected.


        Returns:
            str: A string containing the extracted phone numbers separated by commas
        """

        base_phone_regex = r'[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\d]*\d'  # general_phone_regex
        matches = re.findall(base_phone_regex, self.html.text)  # str(unescape(html.text)))

        matches = [string for string in matches if 6 <= sum(c.isdigit() for c in string) <= 15]
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
