# Requirements

This project requires the following tools: `pandas`, `requests`, `openai`, `python-dotenv`, `selenium`, `undetected-chromedriver`, `openpyxl`, `beautifulsoup4`, `google-generativeai`, `openai`, `setuptools` and `fastapi[standard]`. Additionally, it requires Python 3.8 or newer.

# ENV Files

To use this project, you will need to add `GEMINI_API_KEY` to your .env file, and set it to a valid Google Gemini API key.

# Usage

After cloning this project and setting the correct environmental variables, startup simply requires the command `fastapi dev scraper.py`.

# API Endpoints

The following API endpoints are valid

`scrape`: A GET request which takes the parameters `url` and `name`, with `name` being the name of the firm being scraped. It returns a message containing the scraped data of the firm.
