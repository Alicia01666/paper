from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import pandas as pd
import time

# Setup Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Start the browser maximized
options.add_argument("--disable-extensions")  # Disable browser extensions
options.add_argument("--disable-gpu")  # Disable GPU acceleration
options.add_argument("--no-sandbox")  # Bypass OS security model

# Initialize the Chrome driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Navigate to Myntra's Women's Ethnic Wear category
driver.get("https://www.myntra.com/women-ethnic-wear")

# Function to extract product details from a page
def extract_product_details():
    products = driver.find_elements(By.CLASS_NAME, "product-base")
    for product in products:
        try:
            product_name = product.find_element(By.CLASS_NAME, "product-product").text
            product_brand = product.find_element(By.CLASS_NAME, "product-brand").text
            try:
                current_price_element = product.find_element(By.CLASS_NAME, "product-discountedPrice")
                product_price = current_price_element.text
            except:
                product_price = "N/A"
            try:
                original_price = product.find_element(By.CLASS_NAME, "product-strike").text
            except:
                original_price = "N/A"  # If no original price is found
            product_link = product.find_element(By.TAG_NAME, "a").get_attribute("href")

            product_list.append({
                "Product Name": product_name,
                "Brand": product_brand,
                "Current Price": product_price,
                "Original Price": original_price,
                "Product Link": product_link
            })

        except StaleElementReferenceException:
            print("Element is no longer attached to the DOM.")
            continue
        except Exception as e:
            print(f"An error occurred while extracting product details: {e}")

# Extract product details from the first page
product_list = []
extract_product_details()

# Counter for pages scraped
pages_scraped = 1

# Handle pagination to scrape data from up to 10 pages
while pages_scraped <= 10:
    try:
        # Scroll to the bottom of the page to trigger loading more products
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for the next page to load (increase timeout if necessary)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-base"))
        )
        
        print(f"Page {pages_scraped} loaded, extracting details...")
        # Extract product details from the new page
        extract_product_details()
        
        # Increment page counter
        pages_scraped += 1
        
        # Wait for a short time before checking for more products
        time.sleep(2)

    except TimeoutException:
        print("TimeoutException: Timed out waiting for product details to load.")
        break
    except Exception as e:
        print(f"Error: {e}")
        break

# Close the browser
driver.quit()

# Create a DataFrame and save to Excel
df = pd.DataFrame(product_list)
df.to_excel("scraped_data.xlsx", index=False)

print("Data saved to scraped_data.xlsx")
