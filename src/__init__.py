# This is the main entry point of the application. It imports a function called scrape_jobs from a module called jobspy. scrape_jobs is used to scrape job listings from various websites. These websites include LinkedIn, Indeed, Zip Recruiter, and Glassdoor. The function is called with some parameters to filter the search results. The parameters supplied restrict the job search to "Software Engineer" roles in "Dallas, TX". The search results are limited to 10. Also, the search is limited to the USA on Indeed.
# The number of jobs found is printed to console. The jobs list is also printed to the console.
# Lastly, the resulting job data is written to a CSV file named "jobs.csv". The index=False parameter ensures that the row indices are not written to the CSV file.

# Imports the scrape_jobs function from the jobspy module
from jobspy import scrape_jobs

# Calls the scrape_jobs function to scrape job listings from LinkedIn, Indeed, ZipRecruiter and Glassdoor
# Filters the search to "software engineer" roles in "Dallas, TX"
# Limits the results to 10 listings per site
# Limits Indeed search to USA only
jobs = scrape_jobs(
    site_name=["linkedin", "indeed", "zip_recruiter", "glassdoor"],
    search_term="software engineer",
    location="Dallas, TX",
    results_wanted=10,
    country_indeed='USA'  
)

# Prints number of jobs found to console
print(f"Found {len(jobs)} jobs")

# Prints first 5 job listings to console 
print(jobs.head())

# Exports job listings to a CSV file called jobs.csv
# Does not include row indices in output file
jobs.to_csv("jobs.csv", index=False)

from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["linkedin", "indeed", "zip_recruiter", "glassdoor"],
    search_term="software engineer",
    location="Dallas, TX",
    results_wanted=10,
    country_indeed='USA'  
)
print(f"Found {len(jobs)} jobs")
print(jobs.head())
jobs.to_csv("jobs.csv", index=False)