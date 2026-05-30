# Automated Job Scraper

A Python-based web scraper that extracts remote job listings from [We Work Remotely](https://weworkremotely.com/) and saves them to a CSV file.

## Features

- **Keyword Search:** Search for jobs based on specific keywords (e.g., Python, Javascript, Ruby).
- **Data Extraction:** Collects Job Title, Company Name, Category/Region, and Application Link.
- **Duplicate Prevention:** Ensures that the same job listing is not saved multiple times.
- **CSV Export:** Automatically saves the scraped data into `remote_jobs.csv` for easy analysis.

## Prerequisites

- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tharunguna572006-prog/automated-job-scraper.git
   cd automated-job-scraper
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the scraper from the command line:

```bash
python scraper.py [keyword]
```

Example:
```bash
python scraper.py javascript
```

If no keyword is provided, it defaults to searching for "python" jobs. The results will be saved in `remote_jobs.csv`.

## Project Structure

- `scraper.py`: The main Python script containing the scraping logic.
- `requirements.txt`: List of Python dependencies.
- `remote_jobs.csv`: The output file where job listings are stored.
