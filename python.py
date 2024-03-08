import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_youtube_data():
    # Set up the WebDriver (make sure you have the appropriate webdriver installed and its location in your system PATH)
    driver = webdriver.Chrome()  # Change this line based on your browser choice

    # Navigate to YouTube homepage
    driver.get("https://www.khanacademy.org/science/ap-biology")

    # Find the first few video links on the homepage (you can adjust the range to get more videos)
    video_link = driver.find_element(By.CSS_SELECTOR, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a/yt-formatted-string")

    data = []

    # Click on the video link
    video_link.click()

    # Wait for the video page to load (you may need to adjust the sleep time based on your internet speed)
    driver.implicitly_wait(5)

   
    # Wait for title element
    title_element = driver.find_element((By.CSS_SELECTOR, '#title > h1 > yt-formatted-string'))
    

    # Wait for description element
    description_element = driver.find_element((By.XPATH, '//*[@id="attributed-snippet-text"]/span'))

    # Get the text content of title and description
    title = title_element.text
    description = description_element.text

    # Append the video data to the list
    data.append({'Title': title, 'Description': description})

    # Close the browser window
    driver.quit()
    print(data)
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
