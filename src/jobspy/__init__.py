# Necessary imports
import pandas as pd
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple, Optional

from .jobs import JobType, Location
from .scrapers.indeed import IndeedScraper
from .scrapers.ziprecruiter import ZipRecruiterScraper
from .scrapers.glassdoor import GlassdoorScraper
from .scrapers.linkedin import LinkedInScraper
from .scrapers import ScraperInput, Site, JobResponse, Country
from .scrapers.exceptions import (
    LinkedInException,
    IndeedException,
    ZipRecruiterException,
    GlassdoorException,
)

# Mapping available scraping sites to corresponding scraper class
SCRAPER_MAPPING = {
    Site.LINKEDIN: LinkedInScraper,
    Site.INDEED: IndeedScraper,
    Site.ZIP_RECRUITER: ZipRecruiterScraper,
    Site.GLASSDOOR: GlassdoorScraper,
}

# Helper function to convert string to Site enum object 
def _map_str_to_site(site_name: str) -> Site:
    return Site[site_name.upper()]

# Main function that coordinate the scraping operation from different sites
def scrape_jobs(
    site_name: str | list[str] | Site | list[Site],
    search_term: str,
    location: str = "",
    distance: int = None,
    is_remote: bool = False,
    job_type: str = None,
    easy_apply: bool = False,  
    results_wanted: int = 15,
    country_indeed: str = "usa",
    hyperlinks: bool = False,
    proxy: Optional[str] = None,
    offset: Optional[int] = 0,
) -> pd.DataFrame:
    """
    Simultaneously scrapes job data from multiple job sites.
    :return: results_wanted: pandas dataframe containing job data
    """

    # Helper function to turn string into JobType enum
    def get_enum_from_value(value_str):
        for job_type in JobType:
            if value_str in job_type.value:
                return job_type
        raise Exception(f"Invalid job type: {value_str}")

    job_type = get_enum_from_value(job_type) if job_type else None

    # Creating list of site type(s) to scrap from

    # Defining a function to scrape a single job site
    def scrape_site(site: Site) -> Tuple[str, JobResponse]:
        scraper_class = SCRAPER_MAPPING[site]  # Assigning the appropriate scraper based on the site
        scraper = scraper_class(proxy=proxy)  # Creating an instance of the scraper class

        try:
            # Scraping data from the site using the scraper instance
            scraped_data: JobResponse = scraper.scrape(scraper_input)
        except (LinkedInException, IndeedException, ZipRecruiterException) as lie:
            raise lie  # If a site-specific exception occurs, raise it
        except Exception as e:
            # For non-specific exceptions, raise a site-specific exception based on the site
            if site == Site.LINKEDIN:
                raise LinkedInException(str(e))
            if site == Site.INDEED:
                raise IndeedException(str(e))
            if site == Site.ZIP_RECRUITER:
                raise ZipRecruiterException(str(e))
            if site == Site.GLASSDOOR:
                raise GlassdoorException(str(e))
            else:
                raise e  # For any other exception, raise it
            
        # Upon successful scraping, return the site value and the scraped data
        return site.value, scraped_data  

    site_to_jobs_dict = {}  # Initialize empty dictionary to hold job data from each site

    # Function to be run by each worker in the ThreadPoolExecutor(executes the scrape)
    def worker(site):  
        site_val, scraped_info = scrape_site(site)
        return site_val, scraped_info

    # Scraping of the job sites in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        future_to_site = {executor.submit(worker, site): site for site in scraper_input.site_type}
        for future in concurrent.futures.as_completed(future_to_site):
            site_value, scraped_data = future.result()
            site_to_jobs_dict[site_value] = scraped_data  # Updating the jobs_dict with the job data from the site

    # Retaining the collected job data as list of dataframes
    jobs_dfs: list[pd.DataFrame] = []

    # From each scraped site, convert job listings to a Pandas DataFrame and add to jobs_dfs list
    for site, job_response in site_to_jobs_dict.items():
        # Follow a process of extraction, format, and coversion for each job

    if jobs_dfs:
        jobs_df = pd.concat(jobs_dfs, ignore_index=True)  # Combining all job listing data
        jobs_formatted_df = jobs_df[desired_order]  # Reordering the columns as per the desired order
    else:
        jobs_formatted_df = pd.DataFrame()  # If no jobs data, return an empty dataframe

    return jobs_formatted_df  # Return the resulting dataframe