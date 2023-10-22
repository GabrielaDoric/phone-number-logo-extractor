# phone-number-logo-extractor
Python Web Scraper for Website Logo and Phone Number Extraction

## Description

This project incorporates  web scraping tool designed to extract essential information from websites, including logos, phone numbers, and fax numbers. This tool simplifies the process of gathering contact details and branding assets from web pages, making it a valuable resource for businesses, researchers, and marketing professionals.

## Key Features

Logo Extraction: Program automatically detects and extracts logos from web pages, providing url links to logo images.

Contact Details: Retrieve phone numbers from website content, enabling easy access to contact information for leads and research.

##  Use Cases

Marketing: Quickly obtain company logos and contact details for potential leads and marketing campaigns.

Research: Simplify data collection for research projects, including market analysis and competitor profiling.

Branding: Access high-resolution logos for branding and design purposes.

## Notable Dependencies

Python 3.6 (3.6.8)

BeautifulSoup (for web scraping)

## Getting started

### Installation via pip

In terminal navigate to a project directory: 
`cd .\phone-number-logo-extractor`

Create virtual environment: `python -m venv venv_name`

Activate virtual environment: 
`venv\Scripts\activate`

_*To deactivate virtual environment use `deactivate`_

Install the project dependencies using pip:
`pip install -r requirements.txt`

Once the dependencies are installed, you can run the script with command:
`python extract.py {valid_website_url}`

E.g.
`python extract.py https://www.illion.com.au/`


### Installation via docker

Build docker image:
`docker build -t extractor-app .`

Run image with url as an argument:
`docker run extractor-app {url}`

E.g.
`docker run extractor-app https://www.illion.com.au/`