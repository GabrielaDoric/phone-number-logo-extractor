import argparse
import utils
from extractors.extractor_logo import Extractor_Logo
from extractors.extractor_phone import Extractor_Phone





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





