from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import csv
import io

app = Flask(__name__)

def scrape_jobs(keyword):
    # URL for searching jobs on We Work Remotely
    url = f"https://weworkremotely.com/remote-jobs/search?term={keyword}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    soup = BeautifulSoup(response.text, 'html.parser')
    job_listings = []
    sections = soup.find_all('section', class_='jobs')
    
    for section in sections:
        items = section.find_all('li')
        for item in items:
            if 'view-all' in item.get('class', []):
                continue
                
            try:
                title_tag = item.find('span', class_='title')
                if not title_tag:
                    for tag in item.find_all(['span', 'h3', 'h2']):
                        text = tag.text.strip()
                        if text and "View Company" not in text and len(text) > 5:
                            title_tag = tag
                            break
                
                if not title_tag:
                    continue
                
                title = title_tag.text.strip()
                
                company = "Check Link for Company"
                company_tag = item.find(class_='company')
                if company_tag:
                    company = company_tag.get_text(strip=True)
                else:
                    potential_company = item.find_all('span', class_=False)
                    if len(potential_company) > 0:
                        company = potential_company[0].text.strip()

                category = "Remote / Anywhere"
                region_tag = item.find(class_='region')
                if region_tag:
                    category = region_tag.get_text(strip=True)
                
                links = item.find_all('a')
                job_link = ""
                for a in links:
                    href = a.get('href', '')
                    if '/remote-jobs/' in href and not href.endswith('/remote-jobs/'):
                        job_link = "https://weworkremotely.com" + href if not href.startswith('http') else href
                        break
                
                if title and job_link:
                    if not any(job['Apply Link'] == job_link for job in job_listings):
                        job_listings.append({
                            'Title': title,
                            'Company': company,
                            'Category': category,
                            'Apply Link': job_link
                        })
            except Exception:
                continue

    return job_listings

@app.route('/')
def home():
    keyword = request.args.get('keyword', 'python')
    jobs = scrape_jobs(keyword)
    return jsonify({
        "keyword": keyword,
        "count": len(jobs) if isinstance(jobs, list) else 0,
        "jobs": jobs
    })

if __name__ == "__main__":
    app.run(debug=True)
