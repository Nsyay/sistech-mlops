# 📚 Coursera Course Scraping & Preprocessing Pipeline

This project is the first hands-on task in MLOps portfolio program. I built a pipeline to scrape course information from coursera, collecting data from the first 30 pages. The result is a dataset of 360 courses, each containing details such as the course title, partner, subject, description, rating, level, duration, skills taught, and source URL

## 🦾 Scraping Process
This project uses Selenium to dynamically scrape course data from Coursera. Why? because i want to interact with the browser automatically just like real user

🚨 I already check on coursera's robots.txt and the target endpoint i want scrape is allowed

The scraping process is divided into two steps:
### 1️⃣ Course Card Scraping
1. First, i navigate `Selenium WebDriver` to Coursera's courses list page on [https://www.coursera.org/courses](https://www.coursera.org/courses)
2. On each page, it identifies all `<div data-testid="product-card-cds">` elements that represent course cards then I extract the link `(<a href=...>)` to the course detail page which i assume the link contains either `/specializations/`, `/professional-certificates/`, or `/learn/`
3. After scraping the links from a page, it clicks the "Next Page" button and repeats the process up to a user input maximum page count (in this case i put max_pages=30)
### 2️⃣ Course Detail Scraping
1. For each collected course link, the script opens the detail page and scrapes the following:
    * Title – from `<h1>`
    * Partner – from a `<span>` inside a `div.css-1qp74jq`
    * Subject – from the last breadcrumb `<a class="cds-breadcrumbs-link">`
    * Description – from `<p class="css-4s48ix">`
    * Rating – from `<div aria-label$="stars">`
    * Level – matched by text that ends with "level" using XPath
    * Duration – matched by text that includes "month", "week", "hour", "day", or "schedule" using XPath
    * Skills – extracted from a `<ul class="css-yk0mzy">` list of `<a>` tags representing the skills offered in the course
2. Each course's data is stored in a dictionary, collected into a list, and saved as a csv file

## ⚙️ Preprocessing
After scraping the courses data, I performed a series of preprocessing steps to explore, clean, and structure the data for further analysis or modeling preparation
1. **Missing Values**
   * Filled missing `Rating` values using the **median**
   * Filled missing `Level` values using the **mode**

2. **Unusual Values**
   * Some courses had no valid description — instead showing instructor names
   * These were replaced with the course title as a proxy description

3. **Standardization**
   * Converted all `Duration` values to **hours**:
     - 1 week = 10 hours  
     - 1 month = 4 weeks = 40 hours
   * Replaced "Flexible" durations with the **median** duration value
   * Parsed `Skills` from string format to a **Python list**

4. **Text Cleaning & Lemmatization** (applied to the `Description` column)
   * Converted all text to lowercase
   * Removed numbers and special characters using regex
   * Tokenized the text into individual words
   * Removed English stopwords
   * Lemmatized the tokens into their base forms

before and after example:<br>
**before**: Launch your career as a business analyst. Build job-ready skills for an in-demand career in business analysis in as little as 3 months. No prior experience required to get started.
**after**: launch career business analyst build jobready skill indemand career business analysis little month prior experience required get started

## 🍃 Reflection
During this hands-on, I encountered several challenges, especially due to the dynamic nature of Coursera's website
1.  **Inconsistent HTML Structures**
    * Some elements (like partner name or rating) were missing, changed, or located under slightly different tags/classes across courses
    * Solution: I added multiple fallback strategies using try-except blocks and XPath expressions to locate elements more flexibly
2. **Misplaced Data**
    * Some courses had misleading descriptions (instructor names instead of actual course summaries)
    * Solution: I replaced bad descriptions with the course title
3. **Noisy Data**
    * Raw data including special characters and inconsistent format
    * Solution: I applied text normalization —> lowercasing, regex-based cleaning, stopword removal, standardization, and lemmatization