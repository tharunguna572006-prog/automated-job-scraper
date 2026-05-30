import requests
from bs4 import BeautifulSoup
import csv
import sys

def scrape_jobs(keyword):
    print(f"--- Searching for '{keyword}' jobs on We Work Remotely ---")
    
    # URL for searching jobs on We Work Remotely
    url = f"https://weworkremotely.com/remote-jobs/search?term={keyword}"
    
    # Add a User-Agent to mimic a browser and avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Send a GET request to the website
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Check for HTTP errors
        # Debug: Print a snippet of the response to see if we're getting blocked
        print(f"DEBUG: Response length: {len(response.text)}")
        print(f"DEBUG: Response snippet: {response.text[:200]}") 
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    job_listings = []
    
    # We Work Remotely organizes jobs in sections with class 'jobs'
    sections = soup.find_all('section', class_='jobs')
    
    for section in sections:
        # Each job is usually an <li>
        items = section.find_all('li')
        for item in items:
            # Skip only the 'view-all' link at the bottom of some lists
            if 'view-all' in item.get('class', []):
                continue
                
            try:
                # Target the title
                title_tag = item.find('span', class_='title')
                if not title_tag:
                    # Fallback for title
                    for tag in item.find_all(['span', 'h3', 'h2']):
                        text = tag.text.strip()
                        if text and "View Company" not in text and len(text) > 5:
                            title_tag = tag
                            break
                
                if not title_tag:
                    continue
                
                title = title_tag.text.strip()
                
                # Extract Company - Look for any element with class containing 'company'
                company = "Check Link for Company"
                company_tag = item.find(class_='company')
                if company_tag:
                    company = company_tag.get_text(strip=True)
                else:
                    # Look for the second <a> or a specific span
                    potential_company = item.find_all('span', class_=False)
                    if len(potential_company) > 0:
                        company = potential_company[0].text.strip()

                # Extract Category/Region - Look for class 'region'
                category = "Remote / Anywhere"
                region_tag = item.find(class_='region')
                if region_tag:
                    category = region_tag.get_text(strip=True)
                
                # Extract Link
                links = item.find_all('a')
                job_link = ""
                for a in links:
                    href = a.get('href', '')
                    if '/remote-jobs/' in href and not href.endswith('/remote-jobs/'):
                        job_link = "https://weworkremotely.com" + href if not href.startswith('http') else href
                        break
                
                if title and job_link:
                    # Avoid duplicates
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

def save_to_csv(jobs, filename):
    if not jobs:
        print("No jobs found to save.")
        return

    keys = jobs[0].keys()
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(jobs)
        print(f"Successfully saved {len(jobs)} jobs to {filename}")
    except IOError as e:
        print(f"Error saving to CSV: {e}")

if __name__ == "__main__":
    # Get keyword from command line or use 'python' as default
    search_term = sys.argv[1] if len(sys.argv) > 1 else 'python'
    
    jobs = scrape_jobs(search_term)
    
    if jobs:
        save_to_csv(jobs, 'remote_jobs.csv')
    else:
        print("No jobs found. Try a different keyword like 'javascript' or 'ruby'.")
