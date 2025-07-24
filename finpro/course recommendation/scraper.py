from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def scrape_course_detail(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
    time.sleep(2)

    # Extract course details
    #fetch title
    title = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()

    #fetch partner
    try:
        partner = driver.find_element(By.CSS_SELECTOR, "div.css-1qp74jq span.css-6ecy9b").text.strip()
    except:
        partner = None

    #fetch description
    try:
        description = driver.find_element(By.CSS_SELECTOR, "p.css-4s48ix").text.strip()
    except:
        description = None

    #fetch rating
    try:
        rating_elem = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div[aria-label$="stars"]')
        ))
        rating = rating_elem.text
    except:
        rating = None

    #fetch level and duration
    try:
        level = driver.find_element(By.XPATH, '//div[contains(@class,"css-fk6qfz") and contains(text(), "level")]').text
    except:
        level = None

    try:
        duration = driver.find_element(By.XPATH, '//div[contains(@class, "css-fk6qfz") and (contains(text(), "week") or contains(text(), "hour") or contains(text(), "month") or contains(text(), "day") or contains(text(), "schedule"))]').text
    except:
        duration = None

    
    #fetch skills
    try:
        skills = []
        skill_list = driver.find_elements(By.CSS_SELECTOR, 'ul.css-yk0mzy li a')
        for skill in skill_list:
            text = skill.text.strip()
            if text:
                skills.append(text)
    except:
        skills = []
    
    # fecth subject
    try:
        subject_elem = driver.find_elements(By.CSS_SELECTOR, 'a.cds-breadcrumbs-link')
        subject = subject_elem[-1].text.strip() if subject_elem else None
    except:
        subject = None

    print(f"Title: {title} | Partner: {partner} | Subject: {subject} | Description: {description} | Rating: {rating} | Level: {level} | Duration: {duration} | Skills: {skills}")
    return {"Title": title, "Partner": partner, "Subject": subject, "Description": description, "Rating": rating, "Level": level, "Duration": duration, "Skills": skills, "URL": url}

def scrape_course_card(max_pages=1, output_file="data/coursera_course_details.csv"):
    driver = webdriver.Chrome()
    driver.get("https://www.coursera.org/courses")
    wait = WebDriverWait(driver, 15)

    course_links = set()
    visited = 0

    while visited < max_pages:
        print(f"Collecting course URLs from page {visited + 1}")
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="product-card-cds"]')))
        time.sleep(2)

        # Get all course cards
        cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="product-card-cds"]')
        for card in cards:
            try:
                link = card.find_element(By.TAG_NAME, 'a').get_attribute("href")
                if "/specializations/" in link or "/professional-certificates/" in link or "/learn/" in link:
                    course_links.add(link)
            except:
                continue

        # Click next page
        visited += 1
        try:
            next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Go to next page"]')))
            driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(2)
        except:
            print("Max page reached!")
            break

    print(f"Collected {len(course_links)} course URLs")

    # scrape scrape scrape from detail page yay!
    all_data = []
    for idx, link in enumerate(course_links):
        print(f"[{idx + 1}/{len(course_links)}] Scraping: {link}")
        result = scrape_course_detail(driver, link)
        if result:
            all_data.append(result)

    driver.quit()

    df = pd.DataFrame(all_data)
    df.to_csv(output_file, index=False)
    print(f"\nScraped {len(df)} courses. Saved to {output_file}")

scrape_course_card(max_pages=30)