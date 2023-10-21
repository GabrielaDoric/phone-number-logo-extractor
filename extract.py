import argparse
import utils
import logging
from extractors.extractor_logo import Extractor_Logo
from extractors.extractor_phone import Extractor_Phone

if __name__ == '__main__':

    # Configure and create a logger
    logging.basicConfig(filename='log_file.log', level=logging.DEBUG)
    logger = logging.getLogger("my_logger")

    parser = argparse.ArgumentParser(description='Extract data from a webpage.')
    parser.add_argument('url', type=str, help='URL of the webpage to extract data from')
    args = parser.parse_args()

    try:
        html = utils.get_html(args.url.rstrip('/'))
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        exit(1)

    extractors = [
        Extractor_Phone(html),
        Extractor_Logo(html, args.url)
    ]

    if len(vars(args)) != 1:
        logger.error("Exactly 1 URL argument is required. Use --help for usage information.")
        exit(1)

    for extractor in extractors:
        try:
            print(extractor.extract())
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
