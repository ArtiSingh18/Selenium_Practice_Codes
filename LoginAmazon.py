import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://www.amazon.fr/")
time.sleep(2)

def take_screenshot(name):
    driver.save_screenshot(name)

def scroll_to_element(element):
    driver.execute_script(
         "arguments[0].scrollIntoView({block: 'center'});",
        element
    )

def hover_and_click(element):
    actions = ActionChains(driver)
    actions.move_to_element(element).pause(1).click().perform()

#Search the item
Search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search Amazon.fr']")))
Search.click()
Search.send_keys("Shoes for mens")
assert Search.get_attribute("value") == "Shoes for mens", \
    "Search input verification failed"

#Wait for suggestions
Suggestions = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "sac-suggestion-row-2")))
print("Total suggestions:", Suggestions)
# Assertion: Verify the suggestion is displayed
assert Suggestions.is_displayed(), "Suggestion is not displayed"
Suggestions.click()

#Submit
Submit = driver.find_element(By.XPATH, "//input[@type='submit']")
Submit.click()
time.sleep(2)
# Assertion: Verify search results page is loaded
assert len(driver.find_elements(By.XPATH, "//*[contains(@class,'s-result-item')]")) > 0, \
    "Search results were not loaded"
take_screenshot("Before_filter_shoes_for_mens.png")

# Add Size 44 filter
Size44 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='44']")))
scroll_to_element(Size44)
# Assertion: Verify Size 44 button is displayed
assert Size44.is_displayed(), "Size 44 button is not displayed"
time.sleep(2)
hover_and_click(Size44)
time.sleep(5)
take_screenshot("44_size_Shoes.png")

try:
    # Add PUMA Brand filter
    Brands = driver.find_elements(By.XPATH, "//*[@id='brandsRefinements']//a[@aria-label]")
    for Brand in Brands:
        scroll_to_element(Brand)
        print("Brand:", Brand.text)
        if Brand.text.strip() == "PUMA":
            time.sleep(2)
            Brand.click()
            print("clicked on",Brand.text)
            #ActionChains(driver).move_to_element(Brand).pause(1).click().perform()
            time.sleep(4)
            take_screenshot("PUMA_Shoes.png")
            time.sleep(2)
            break
        else:
            print(f"Brand - {Brand.text}")
except Exception as e:
    print("Search input test failed Brand:", e)

try:
    #Add Black colour filter
    Colour = driver.find_element(By.ID, "p_n_g-1004232833091/14223299031")
    scroll_to_element(Colour)
    time.sleep(2)
    hover_and_click(Colour)
    time.sleep(2)
    take_screenshot("Black_shoes.png")
    time.sleep(2)

except Exception as e:
    print("Search input test failed:", e)

take_screenshot("after_flter_shoes_for_mens.png")
driver.quit()