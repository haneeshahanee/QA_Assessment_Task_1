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
initial_rows = driver.find_elements(By.CSS_SELECTOR, ".rt-tbody .rt-tr-group")
initial_row_count = len([row for row in initial_rows if row.text.strip()])
```

I used a list comprehension to filter out empty rows by checking if `row.text.strip()` returns any content. This gives me only the actual data rows, not the empty placeholders.

### Step 2: Adding a New Person

For this step, I needed to click the "Add" button and fill out the registration form. I organized the test data in a dictionary to keep it clean and maintainable:

```python
new_person = {
    "firstName": "Haneesha",
    "lastName": "Molleti",
    "email": "haneesha.molleti@example.com",
    "age": "24",
    "salary": "50000",
    "department": "Engineering"
}
```

I used explicit waits to ensure the form was fully loaded before interacting with it:
```python
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.ID, "firstName")))
```

This prevents timing issues where we might try to fill fields before they're ready.

### Step 3: Verifying Row Count Increased

After adding the new person, I repeated the same row counting logic and used an assertion to verify the count increased by exactly 1:

```python
assert updated_row_count == initial_row_count + 1, \
    f"Expected {initial_row_count + 1} rows, but found {updated_row_count}"
```

The assertion includes a descriptive error message that shows what was expected versus what was found, making debugging easier if something goes wrong.

### Step 4: Editing the Person's Age

This was the trickiest part because of potential issues with element interception from ads and overlays on the DemoQA website.

**My solution involved several strategies:**

1. **Finding the correct row:**
```python
for row in all_rows:
    if new_person["firstName"] in row.text and new_person["lastName"] in row.text:
        target_row = row
        break
```

2. **Handling click interception:**
The DemoQA website has advertisements that can block clicks, so I implemented multiple fallback methods:

```python
# Method 1: Regular click
try:
    edit_button.click()
    click_successful = True
except ElementClickInterceptedException:
    # Try alternative methods...
```

If the regular click fails, I fall back to:
- **JavaScript click:** Bypasses some overlay issues by executing the click directly through JavaScript
- **ActionChains:** Simulates actual mouse movement to the element before clicking

3. **Removing ads proactively:**
```python
driver.execute_script("""
    var ads = document.querySelectorAll('iframe[id*="google_ads"], iframe[title*="ad"]');
    ads.forEach(function(ad) { ad.remove(); });
""")
```

I also scrolled the edit button into view to ensure it's visible and clickable:
```python
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_button)
```

### Step 5: Verifying the Age Update

Finally, I verified that the age was actually updated in the table by searching for the row again and checking if the new age value appears in its text:

```python
for row in all_rows:
    if new_person["firstName"] in row.text and new_person["lastName"] in row.text:
        if new_age in row_text:
            age_verified = True
            break
```

## 🎯 Key Design Decisions

### 1. Error Handling
I wrapped the entire test in a try-except-finally block:
- **Try:** Execute all test steps
- **Except:** Capture errors, print meaningful messages, and save a screenshot
- **Finally:** Clean up by closing the browser (even if tests fail)

This ensures the browser doesn't stay open if something crashes, and I get visual debugging information through screenshots.

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
Step 1: Counting initial rows...
Initial row count: 3

Step 2: Adding a new person...
Added new person: Haneesha Molleti

Step 3: Verifying row count increased...
Row count increased from 3 to 4

Step 4: Finding and editing the new person's age...
Changed age from 24 to 20

Step 5: Verifying age update...
Age successfully updated to 20 in the table

=== ALL TESTS PASSED ===
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
├── README.md               # This file - explains my solution
├── .gitignore              # Excludes unnecessary files from git
└── error_screenshot.png    # Generated automatically if test fails
```

## 🔧 Dependencies

My solution requires these Python packages (listed in `requirements.txt`):

```
selenium==4.27.1
webdriver-manager==4.0.2
```

The webdriver-manager package automatically handles ChromeDriver installation and updates, so you don't need to manually download the driver.

## ✅ Test Validation

My solution includes several assertions to validate each requirement:

1. **Row count assertion:** Verifies exactly one row was added
2. **Element existence assertion:** Confirms the new person's row exists
3. **Click success assertion:** Ensures the edit button was clicked successfully
4. **Age update assertion:** Validates the age field shows the updated value

If any assertion fails, you'll see a descriptive error message and a screenshot will be saved.

## 🎓 What I Learned

Through this exercise, I learned:
- How to handle dynamic web tables with Selenium
- Strategies for dealing with unpredictable web elements (ads, overlays)
- The importance of explicit waits for reliable automation
- How to implement robust error handling in test automation
- Best practices for organizing test data and making code maintainable

## 📝 Future Improvements

If I were to extend this solution, I would:
- Use a testing framework like pytest for better test organization
- Add parameterized tests to test with multiple different users
- Implement Page Object Model (POM) for better code structure
- Add more detailed logging instead of print statements
- Create a test report with pass/fail statistics

## 👤 Author

Created by Haneesha Molleti as part of a QA automation assessment.

---

**Note:** This is a demonstration project showing practical Selenium automation skills with Python. The test interacts with a live demo website, so occasional changes to the site structure might require updates to the selectors.