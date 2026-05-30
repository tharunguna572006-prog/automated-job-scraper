# Automated Job Scraper API

A Python-based web API that extracts remote job listings from [We Work Remotely](https://weworkremotely.com/) and returns them in JSON format. This project is configured to be hosted on Vercel as a Serverless Function.

## Features

- **Web API:** Access job listings via a simple URL.
- **Keyword Search:** Search for jobs by passing a `keyword` query parameter.
- **JSON Response:** Returns job data (Title, Company, Category, Apply Link) in a structured JSON format.
- **Vercel Ready:** Optimized for deployment on Vercel using Flask.

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

## Local Usage

Run the Flask application locally:

```bash
python main.py
```

Access the API at `http://127.0.0.1:5000/?keyword=python`.

## Deployment on Vercel

This project is ready for Vercel. Simply push your changes to GitHub and connect your repository to Vercel. It will automatically detect `main.py` as the entrypoint.

## API Endpoint

- `GET /?keyword=[term]`
- Default keyword: `python`

## Project Structure

- `main.py`: The Flask application and scraping logic.
- `requirements.txt`: List of Python dependencies (including `flask`).
