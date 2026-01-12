# Task 1 #

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://demoqa.com/webtables")
driver.maximize_window()
wait = WebDriverWait(driver, 10)

# Step 1: Count initial rows
rows = driver.find_elements(By.XPATH, "//div[@class='rt-tbody']//div[@role='rowgroup']")
initial_count = len([r for r in rows if r.text.strip()])
print(f"Step 1: Initial rows = {initial_count}")

# Step 2: Add new person
driver.find_element(By.ID, "addNewRecordButton").click()
wait.until(EC.visibility_of_element_located((By.ID, "firstName")))

driver.find_element(By.ID, "firstName").send_keys("Haneesha")
driver.find_element(By.ID, "lastName").send_keys("Molleti")
driver.find_element(By.ID, "userEmail").send_keys("haneeshamolleti@gmail.com")
driver.find_element(By.ID, "age").send_keys("24")
driver.find_element(By.ID, "salary").send_keys("50000")
driver.find_element(By.ID, "department").send_keys("Engineering")
driver.find_element(By.ID, "submit").click()
print("Step 2: Person added")

# Step 3: Verify row count increased
time.sleep(0.5)
rows = driver.find_elements(By.XPATH, "//div[@class='rt-tbody']//div[@role='rowgroup']")
new_count = len([r for r in rows if r.text.strip()])
print(f"Step 3: New count = {new_count} (Increased: {new_count > initial_count})")

# Step 4: Edit the person's age
rows = driver.find_elements(By.XPATH, "//div[@class='rt-tbody']//div[@role='rowgroup']")
for row in rows:
    if "Haneesha" in row.text and "Molleti" in row.text:
        edit_btn = row.find_element(By.XPATH, ".//span[@title='Edit']")
        driver.execute_script("arguments[0].click();", edit_btn)
        break

wait.until(EC.visibility_of_element_located((By.ID, "age")))
driver.find_element(By.ID, "age").clear()
driver.find_element(By.ID, "age").send_keys("20")
driver.find_element(By.ID, "submit").click()
print("Step 4: Age edited to 20")

# Step 5: Verify age updated
time.sleep(0.5)
rows = driver.find_elements(By.XPATH, "//div[@class='rt-tbody']//div[@role='rowgroup']")
for row in rows:
    if "Haneesha" in row.text and "20" in row.text:
        print("Step 5: Age verified = 20")
        break

time.sleep(2)
driver.quit()
print("\nAll steps completed!")
