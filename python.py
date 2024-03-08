import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_youtube_data():
    # Set up the WebDriver (make sure you have the appropriate webdriver installed and its location in your system PATH)
    driver = webdriver.Chrome()  # Change this line based on your browser choice

    # Navigate to YouTube homepage
    driver.get("https://www.youtube.com/playlist?list=PL7A9646BC5110CF64")


    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#contents"))
    )

    main = driver.find_element(By.ID,"contents")
    # Find the first few video links on the homepage (you can adjust the range to get more videos)
    video_link = main.find_element(By.ID,"thumbnail")

    video_link.click()

    driver.implicitly_wait(5)


    data = []


   
    # Wait for title element
    title_element = driver.find_element(By.XPATH, '//*[@id="title"]/h1/yt-formatted-string')
    title = title_element.text

    # Wait for description element

    
    description = driver.find_element(By.XPATH, '//*[@id="description"]')

    
    description_short = description.find_element(By.XPATH, '//*[@id="description-inner"]')
    description_short.click()


    description_element = description.find_element(By.XPATH, '//*[@id="description-inline-expander"]/yt-attributed-string/span')

    # Get the text content of title and description
    title = title_element.text
    description = description_element.text

    # Append the video data to the list
    data.append({'Title': title, 'Description': description})

    # Close the browser window
    driver.quit()

    return data

def write_to_csv(data):
    # Specify the CSV file path
    csv_file_path = 'youtube_data.csv'

    # Write the data to the CSV file
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Title', 'Description']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the data rows
        writer.writerows(data)

if __name__ == "__main__":
    youtube_data = scrape_youtube_data()
    write_to_csv(youtube_data)
