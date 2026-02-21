import requests
from bs4 import BeautifulSoup
import sqlite3
from classifier import classify_opportunity
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DB_PATH = "database/ivyintel.db"


# Connect database
def connect_db():
    return sqlite3.connect(DB_PATH)


# Check duplicate before inserting
def opportunity_exists(title, university):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM opportunities WHERE title=? AND university=?",
        (title, university)
    )

    exists = cursor.fetchone()

    conn.close()

    return exists is not None


# Save opportunity safely
def save_opportunity(title, university, description, deadline, link):

    if opportunity_exists(title, university):
        return

    category = classify_opportunity(title + " " + description)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO opportunities
        (title, university, category, description, deadline, link)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, university, category, description, deadline, link))

    conn.commit()
    conn.close()


# Common title filter
def is_valid_title(title):

    if not title:
        return False

    title_lower = title.lower()

    ignore_words = [
        "skip to main content",
        "search",
        "menu",
        "home",
        "about",
        "contact",
        "login",
        "sign in",
        "register",
        "privacy",
        "accessibility"
    ]

    if any(word in title_lower for word in ignore_words):
        return False

    if len(title) < 15:
        return False

    return True


# Generic scraper function
def scrape_university(base_url, university_name):

    try:

        response = requests.get(base_url, verify=False, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.select("a[href]")

        count = 0

        for link_tag in links:

            title = link_tag.get_text(strip=True)

            if not is_valid_title(title):
                continue

            link = link_tag.get("href")

            if not link:
                continue

            if not link.startswith("http"):
                link = base_url + link

            save_opportunity(
                title=title,
                university=university_name,
                description=f"{university_name} opportunity",
                deadline="Check website",
                link=link
            )

            count += 1

            if count >= 30:
                break

        print(f"{university_name}: {count} opportunities saved")

    except Exception as e:

        print(f"{university_name} scraping error:", e)


# Individual university scrapers
def scrape_harvard():
    scrape_university(
        "https://college.harvard.edu/events",
        "Harvard"
    )


def scrape_yale():
    scrape_university(
        "https://yalecollege.yale.edu/events",
        "Yale"
    )


def scrape_princeton():
    scrape_university(
        "https://www.princeton.edu/events",
        "Princeton"
    )


def scrape_columbia():
    scrape_university(
        "https://www.columbia.edu/events",
        "Columbia"
    )


def scrape_upenn():
    scrape_university(
        "https://www.upenn.edu/events",
        "UPenn"
    )


# Main function
def scrape_all():

    print("Starting Ivy League scraping...")

    scrape_harvard()
    scrape_yale()
    scrape_princeton()
    scrape_columbia()
    scrape_upenn()

    print("All Ivy League opportunities scraped successfully.")