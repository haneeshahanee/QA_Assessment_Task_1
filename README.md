# Selenium Web Tables Automation - Solution

This repository contains my solution to the QA automation exercise for testing web table operations on the DemoQA website using Selenium WebDriver and Python.

## 📋 The Task

I was given the following challenge:

**Website:** [DemoQA - Web Tables](https://demoqa.com/webtables)

**Requirements:**
1. Count how many rows currently exist in the table
2. Click the "Add" button and fill out the form to add a new person
3. Verify that the row count has increased by 1
4. Find the row containing the newly added person and click the "Edit" (pencil) icon to change their age
5. Verify the age has been updated in the table

## 🛠️ Technologies Used

- **Python** 3.8+
- **Selenium WebDriver** 4.x
- **Chrome WebDriver**

## 🚀 How to Run My Solution

### Prerequisites

Make sure you have:
- Python 3.8 or higher installed
- Google Chrome browser
- pip package manager

### Installation Steps

1. **Clone this repository:**
```bash
git clone https://github.com/yourusername/selenium-web-tables-automation.git
cd selenium-web-tables-automation
```

2. **Create a virtual environment (recommended):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the test:**
```bash
python test_web_tables.py
```

The Chrome browser will open automatically, perform all the test steps, and you'll see the results in your terminal.

## 💡 My Solution Approach

### Step 1: Counting Initial Rows

The first challenge was to accurately count the rows in the table. The DemoQA table uses a library that creates empty placeholder rows, so I couldn't just count all elements with the `.rt-tr-group` class.

**My approach:**
```python
rows = driver.find_elements(By.XPATH, "//div[@class='rt-tbody']//div[@role='rowgroup']")
initial_count = len([r for r in rows if r.text.strip()])
```

I used a list comprehension to filter out empty rows by checking if `row.text.strip()` returns any content. This gives me only the actual data rows, not the empty placeholders.

### Step 2: Adding a New Person

For this step, I needed to click the "Add" button and fill out the registration form. I organized the test data in a dictionary to keep it clean and maintainable:

```python
new_person = {
    "firstName": "Haneesha",
    "lastName": "Molleti",
    "email": "haneeshamolleti04@gmail.com",
    "age": "24",
    "salary": "50000",
    "department": "Engineering"
}
```

I used explicit waits to ensure the form was fully loaded before interacting with it:
```python
driver.find_element(By.ID, "addNewRecordButton").click()
wait.until(EC.visibility_of_element_located((By.ID, "firstName")))

driver.find_element(By.ID, "firstName").send_keys("Haneesha")
driver.find_element(By.ID, "lastName").send_keys("Molleti")
# ... other fields
driver.find_element(By.ID, "submit").click()
```

This prevents timing issues where we might try to fill fields before they're ready.

### Step 3: Verifying Row Count Increased

After adding the new person, I repeated the same row counting logic and verified the count increased:

```python
time.sleep(0.5)
rows = driver.find_elements(By.XPATH, "//div[@class='rt-tbody']//div[@role='rowgroup']")
new_count = len([r for r in rows if r.text.strip()])
print(f"Step 3: New count = {new_count} (Increased: {new_count > initial_count})")
```

### Step 4: Editing the Person's Age

This was the trickiest part because of potential issues with element interception from ads and overlays on the DemoQA website.

**My solution involved several strategies:**

1. **Finding the correct row:**
```python
for row in rows:
    if "Haneesha" in row.text and "Molleti" in row.text:
        edit_btn = row.find_element(By.XPATH, ".//span[@title='Edit']")
        driver.execute_script("arguments[0].click();", edit_btn)
        break
```
I iterate through all rows and search for both first name AND last name to ensure uniqueness.
2. **Using JavaScript click:**
Instead of using the regular .click() method, I used JavaScript execution to click the edit button:
```Python
driver.execute_script("arguments[0].click();", edit_btn)
```
This bypasses overlay issues from advertisements that might block normal clicks.
3. **Updating the age:**
```Python
wait.until(EC.visibility_of_element_located((By.ID, "age")))
driver.find_element(By.ID, "age").clear()
driver.find_element(By.ID, "age").send_keys("20")
driver.find_element(By.ID, "submit").click()
```
I wait for the form to appear, clear the existing age value, and enter the new age (20).

### Step 5: Verifying the Age Update

Finally, I verified that the age was actually updated in the table by searching for the row again and checking if the new age value appears in its text:

```python
for row in rows:
    if "Haneesha" in row.text and "20" in row.text:
        print("Step 5: Age verified = 20")
        break
```

## 🎯 Key Design Decisions

### 1. XPath Over CSS Selectors
I chose XPath selectors for better readability and reliability:
- By.XPATH, "//div[@class='rt-tbody']//div[@role='rowgroup']" clearly shows we're targeting row groups within the table body
- XPath provides more flexibility for complex DOM traversal

### 2. Explicit Waits vs. Implicit Waits
I chose explicit waits (`WebDriverWait`) over implicit waits because:
- More control over what condition we're waiting for
- Better performance (only waits when needed)
- Clearer code that shows exactly what we're waiting for

### 3. Multiple Click Strategies
The multiple click methods (regular, JavaScript, ActionChains) ensure robustness across different scenarios. Some websites work better with JavaScript clicks, others need the actual mouse movement from ActionChains.

### 4. Clear Console Output
I added print statements at each step so anyone running the test can follow along and see exactly what's happening:
```python
print(f"Added new person: {new_person['firstName']} {new_person['lastName']}")
print(f"Changed age from {new_person['age']} to {new_age}")
```

## 📊 Expected Output

When you run the test, you'll see:

```
Step 1: Initial rows = 3
Step 2: Person added
Step 3: New count = 4 (Increased: True)
Step 4: Age edited to 20
Step 5: Age verified = 20

All steps completed!
```

The browser will stay open for 3 seconds after completion so you can see the final state of the table.

## 🐛 Challenges I Faced and How I Solved Them

### Challenge 1: Empty Placeholder Rows
**Problem:** The table library creates empty divs that look like rows but contain no data.
**Solution:** Used `row.text.strip()` to filter out rows with no visible text content.

### Challenge 2: Click Interception from Ads
**Problem:** The DemoQA website has advertisements that sometimes cover clickable elements.
**Solution:** Implemented JavaScript to remove ad iframes and used multiple click strategies as fallbacks.

### Challenge 3: Timing Issues
**Problem:** Elements might not be immediately available after actions.
**Solution:** Used explicit waits with `WebDriverWait` and added small `time.sleep()` delays where needed for DOM updates.

### Challenge 4: Finding the Correct Row
**Problem:** Multiple rows could theoretically have similar data.
**Solution:** Used both first name AND last name in the search condition to ensure uniqueness.

## 📁 Project Structure

```
selenium-web-tables-automation/
├── test_web_tables.py      # Main test script with all automation logic
├── requirements.txt         # Python dependencies (selenium, webdriver-manager)
README.md  
```

## 🔧 Dependencies

My solution requires these Python packages (listed in `requirements.txt`):

```
selenium==4.27.1
webdriver-manager==4.0.2
```

The webdriver-manager package automatically handles ChromeDriver installation and updates, so you don't need to manually download the driver.

## ✅ Test Validation

My solution validates each requirement:

1.Initial row count: Prints the starting number of rows
2.Row addition: Confirms person was added successfully
3.Row count increase: Verifies the count increased (shows boolean True/False)
4.Age edit: Confirms age was changed to 20
5.Age verification: Validates the new age appears in the table
