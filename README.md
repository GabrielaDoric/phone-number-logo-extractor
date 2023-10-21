# phone-number-logo-extractor
Python Web Scraper for Website Logo and Phone Number Extraction

## Description


## Usage

#### Installation via pip

Python version used in project: 3.6.8.

In terminal navigate to a project directory:

`cd .\phone-number-logo-extractor`

Create virtual environment

`python -m venv venv`

`venv\Scripts\activate`

Install the project dependencies using pip:

`pip install -r requirements.txt`

Once the dependencies are installed, you can run the script:

`python extract.py {valid_website_url}`


#### Installation via docker

Build image
`docker build -t extractor-app .`

Run image with url as an argument
`docker run extractor-app https://www.illion.com.au/`