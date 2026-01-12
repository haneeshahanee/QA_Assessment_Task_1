# Task 1 #

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import time


def test_web_tables():
    """
    Main test function for web table operations.
    Tests adding and editing records in the DemoQA web tables.
    """
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()

    try:
        # Navigating to DemoQA Web Tables page
        driver.get("https://demoqa.com/webtables")
        driver.maximize_window()

        # Removing advertisements that might interfere with element interactions
        try:
            driver.execute_script("""
                var ads = document.querySelectorAll('iframe[id*="google_ads"], iframe[title*="ad"]');
                ads.forEach(function(ad) { ad.remove(); });
            """)
        except:
            pass

        # STEP 1: we need to count how many rows currently exist in the table
       
        print("Step 1: Counting initial rows...")
        initial_rows = driver.find_elements(By.CSS_SELECTOR, ".rt-tbody .rt-tr-group")
        # Filter out empty placeholder rows (rows with no text)
        initial_row_count = len([row for row in initial_rows if row.text.strip()])
        print(f"Initial row count: {initial_row_count}")

        # STEP 2: Click the "Add" button and fill out the form

        print("\nStep 2: Adding a new person...")
        add_button = driver.find_element(By.ID, "addNewRecordButton")
        add_button.click()

        # Wait for the registration form modal to appear
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.ID, "firstName")))

        # Define the new person data
        new_person = {
            "firstName": "Haneesha",
            "lastName": "Molleti",
            "email": "haneeshamolleti04@gmail.com",
            "age": "24",
            "salary": "50000",
            "department": "Engineering"
        }

        # Fill out each field in the form
        driver.find_element(By.ID, "firstName").send_keys(new_person["firstName"])
        driver.find_element(By.ID, "lastName").send_keys(new_person["lastName"])
        driver.find_element(By.ID, "userEmail").send_keys(new_person["email"])
        driver.find_element(By.ID, "age").send_keys(new_person["age"])
        driver.find_element(By.ID, "salary").send_keys(new_person["salary"])
        driver.find_element(By.ID, "department").send_keys(new_person["department"])

        # Submit the form
        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        print(f"Added new person: {new_person['firstName']} {new_person['lastName']}")

        # STEP 3: Now verifying that the row count has increased by 1

        print("\nStep 3: Verifying row count increased...")
        time.sleep(0.5)  # Small wait for DOM to update
        updated_rows = driver.find_elements(By.CSS_SELECTOR, ".rt-tbody .rt-tr-group")
        updated_row_count = len([row for row in updated_rows if row.text.strip()])

        # Assert that exactly one row was added
        assert updated_row_count == initial_row_count + 1, \
            f"Expected {initial_row_count + 1} rows, but found {updated_row_count}"
        print(f"Row count increased from {initial_row_count} to {updated_row_count}")

        # STEP 4: Finding the new person's row and click Edit to change age

        print("\nStep 4: Finding and editing the new person's age...")
        new_age = "20"

        # Get all table rows
        all_rows = driver.find_elements(By.CSS_SELECTOR, ".rt-tbody .rt-tr-group")

        # Locate the row containing our newly added person
        target_row = None
        for row in all_rows:
            if new_person["firstName"] in row.text and new_person["lastName"] in row.text:
                target_row = row
                break

        assert target_row is not None, "Could not find the newly added person in the table"

        # Find the Edit button (pencil icon) in that row
        edit_button = target_row.find_element(By.CSS_SELECTOR, "span[title='Edit']")

        # Scroll the edit button into view to ensure it's clickable
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_button)
        time.sleep(0.5)

        # Remove any overlaying ads again before clicking
        driver.execute_script("""
            var ads = document.querySelectorAll('iframe[id*="google_ads"], iframe[title*="ad"]');
            ads.forEach(function(ad) { ad.remove(); });
        """)
        time.sleep(0.3)

        # Try multiple methods to click the edit button (handles click interception)
        click_successful = False

        # Method 1: Regular Selenium click
        try:
            edit_button.click()
            click_successful = True
        except ElementClickInterceptedException:
            print("Regular click blocked, trying alternative methods...")

        # Method 2: JavaScript click (bypasses some overlay issues)
        if not click_successful:
            try:
                driver.execute_script("arguments[0].click();", edit_button)
                click_successful = True
                print("Used JavaScript click")
            except:
                pass

        # Method 3: ActionChains click (moves mouse and clicks)
        if not click_successful:
            try:
                actions = ActionChains(driver)
                actions.move_to_element(edit_button).click().perform()
                click_successful = True
                print("Used ActionChains click")
            except:
                pass

        assert click_successful, "Could not click the edit button with any method"

        # Wait for the edit form to appear
        wait.until(EC.visibility_of_element_located((By.ID, "age")))

        # Clear the existing age and enter the new age
        age_field = driver.find_element(By.ID, "age")
        age_field.clear()
        age_field.send_keys(new_age)

        # Submit the changes
        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        print(f"Changed age from {new_person['age']} to {new_age}")

        # STEP 5: Verify the age has been updated in the table
        
        print("\nStep 5: Verifying age update...")
        time.sleep(0.5)  # Small wait for DOM to update

        # Find the row again and verify the age
        all_rows = driver.find_elements(By.CSS_SELECTOR, ".rt-tbody .rt-tr-group")

        age_verified = False
        for row in all_rows:
            if new_person["firstName"] in row.text and new_person["lastName"] in row.text:
                row_text = row.text
                if new_age in row_text:
                    age_verified = True
                    print(f"Age successfully updated to {new_age} in the table")
                    break

        assert age_verified, f"Could not verify that age was updated to {new_age}"

        print("\n=== ALL TESTS PASSED ===")

    except Exception as e:
        # If any error occurs, print it and save a screenshot for debugging
        print(f"\nTEST FAILED: {str(e)}")
        driver.save_screenshot("error_screenshot.png")
        print("Screenshot saved as 'error_screenshot.png'")
        raise

    finally:
        # Keep browser open for 3 seconds to view the final state
        time.sleep(3)
        # Clean up: close the browser
        driver.quit()


if __name__ == "__main__":
    test_web_tables()