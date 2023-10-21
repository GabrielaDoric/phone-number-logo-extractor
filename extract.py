import argparse
import utils
import logo_extractor as logo
import phone_extractor as phone
from Extractor_Logo import Extractor_Logo
from Extractor_Phone import Extractor_Phone


def extract(url):
    html = utils.get_html(url.rstrip('/'))

    logo_url = logo.extract(html, url)

    phone_numbers = phone.extract(html, url)

    return phone_numbers, logo_url


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract data from a webpage.')
    parser.add_argument('url', type=str, help='URL of the webpage to extract data from')
    args = parser.parse_args()

    html = utils.get_html(args.url.rstrip('/'))
    extractors = [
        Extractor_Phone(html),
        Extractor_Logo(html, args.url)
    ]

    if len(vars(args)) != 1:
        print("Exactly 1 URL argument is required. Use --help for usage information.")
        exit(1)

    try:
        for extractor in extractors:
            print(extractor.extract())
    except KeyboardInterrupt:
        print("Extraction process interrupted.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")





