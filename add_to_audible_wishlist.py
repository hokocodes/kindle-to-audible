from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import getpass

failed_asins = []
def setup_driver():
    """Set up Chrome WebDriver with basic configuration"""
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def login_to_audible(driver):
    """Log in to Audible account"""
    driver.get("https://www.audible.com/sign-in")
    

    print("Please sign in manually. Program will continue once you have successfully signed in.")
    while True:
        time.sleep(1)
        if "Explore" in driver.page_source:
            break

def add_to_wishlist(driver, asin):
    """Add a book to wishlist using its ASIN"""
    try:
        driver.get("https://www.audible.com/")
                # Wait for search bar and enter ASIN
        search_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "header-search"))
        )
        search_bar.clear()
        search_bar.send_keys(asin)


        # Wait for search results and click first result
        first_result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "results-item-0"))
        )
        driver.execute_script("arguments[0].click();", first_result)

        
        # Wait for search results and click first result
        moreoptions = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "discovery_buyBox_moreOptions"))
        )
        moreoptions.click()

        # Wait for 'Add to Wish List' button by ID and click if available
        add_to_wishlist_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "adbl-add-to-wishlist-button"))
        )
        add_to_wishlist_button.click()



    except Exception as e:
        print(f"Failed to add ASIN {asin}: {str(e)}")
        failed_asins.append(asin)
        return False

def read_asins_from_csv(csv_file):
    """Read ASINs from CSV file"""
    asins = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header if exists
        for row in csv_reader:
            if row and row[1]:  # Ensure row is not empty and has ASIN
                asins.append(row[1].strip())
    return asins

def main():
    # Get user credentials

    csv_file = "kindle_books.csv"
    
    # Initialize driver
    driver = setup_driver()
    
    try:
        # Log in to Audible
        login_to_audible(driver)
        
        # Read ASINs from CSV
        asins = read_asins_from_csv(csv_file)
        
        # Add each book to wishlist
        success_count = 0
        total_count = len(asins)
        
        for asin in asins:
            if add_to_wishlist(driver, asin):
                success_count += 1
            time.sleep(2)  # Delay to avoid overwhelming the server
        
        print(f"\nCompleted! Successfully added {success_count}/{total_count} books to wishlist. Failed ASINs: {failed_asins}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()