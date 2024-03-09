import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI
import os


def scrape_youtube_data():
    counter = 0
    for original_videos in video_links:

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#contents"))
        )
         
        new_main = driver.find_element(By.ID,"contents")
        newVideoLinks = new_main.find_elements(By.CSS_SELECTOR, 'a.ytd-thumbnail')
        
        video = newVideoLinks[counter]

        video.click()

        driver.implicitly_wait(5)

        data = []

        # Wait for title element
        title_element = driver.find_element(By.XPATH, '//*[@id="title"]/h1/yt-formatted-string')
        title = title_element.text

        # Wait for description element

        
        description_html = driver.find_element(By.XPATH, '//*[@id="description"]')

        
        description_short = description_html.find_element(By.XPATH, '//*[@id="description-inner"]')
        description_short.click()


        description_element = description_html.find_element(By.XPATH, '//*[@id="description-inline-expander"]/yt-attributed-string/span')

        # Get the text content of title and description
        title = title_element.text
        firstDescription = description_element.text

        video_elements_container = driver.find_element(By.XPATH, '//*[@id="items"]')
        video_elements = video_elements_container.find_elements(By.XPATH,'//*[@id="details"]/h4[1]')

        video_element_content = ""

        for element in video_elements:

            element_text = element.text
            video_element_content += " " + element_text

        description = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Summarize {firstDescription} relating to biology and in 10 words without any commas in the message, which is related to {title}"},
        ],
        temperature=0,
        )

        data.append({'Title': title, 'Description': description.choices[0].message.content, 'Elements': video_element_content})

        driver.get("https://www.youtube.com/playlist?list=PL7A9646BC5110CF64")

        write_to_csv(data)

        counter += 1

    driver.quit()
    
    # Append the video data to the list

def write_to_csv(data):
    # Specify the CSV file path
    csv_file_path = 'youtube_data.csv'

    # Write the data to the CSV file
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Title', 'Description', 'Elements']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the data rows
        writer.writerows(data)

if __name__ == "__main__":
    client = OpenAI(api_key="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")
    driver = webdriver.Chrome()  # Change this line based on your browser choice

    # Navigate to YouTube homepage
    driver.get("https://www.youtube.com/playlist?list=PL7A9646BC5110CF64")


    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#contents"))
    )

    main = driver.find_element(By.ID,"contents")
    # Find the first few video links on the homepage (you can adjust the range to get more videos)

    video_links = main.find_elements(By.ID,"thumbnail")

    scrape_youtube_data()
