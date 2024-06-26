import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from openai import OpenAI
import os


def scrape_youtube_data():
    counter = 0
    for original_videos in video_links:

        if counter <= 99:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#contents"))
            )


        if counter > 99:

            new_main = driver.find_element(By.ID,"contents")
            newVideoLinks = new_main.find_elements(By.CSS_SELECTOR, 'a.ytd-thumbnail')
            # Scroll to the bottom of the playlist
            driver.execute_script("arguments[0].scrollIntoView(true);", newVideoLinks[99])

            WebDriverWait(driver, 10)
            while True:
                video_count = driver.execute_script("return document.querySelectorAll('ytd-playlist-video-renderer').length;")
                if video_count > 100:
                    break

            if counter > 199:
                new_main = driver.find_element(By.ID,"contents")
                newVideoLinks = new_main.find_elements(By.CSS_SELECTOR, 'a.ytd-thumbnail')
                driver.execute_script("arguments[0].scrollIntoView(true);", newVideoLinks[199])
                WebDriverWait(driver, 10)
                while True:
                    video_count = driver.execute_script("return document.querySelectorAll('ytd-playlist-video-renderer').length;")
                    if video_count > 200:
                        break
                if counter > 299:
                    new_main = driver.find_element(By.ID,"contents")
                    newVideoLinks = new_main.find_elements(By.CSS_SELECTOR, 'a.ytd-thumbnail')
                    driver.execute_script("arguments[0].scrollIntoView(true);", newVideoLinks[299])
                    WebDriverWait(driver, 10)
                    while True:
                        video_count = driver.execute_script("return document.querySelectorAll('ytd-playlist-video-renderer').length;")
                        if video_count > 300:
                            break
                    if counter > 399:
                        new_main = driver.find_element(By.ID,"contents")
                        newVideoLinks = new_main.find_elements(By.CSS_SELECTOR, 'a.ytd-thumbnail')
                        driver.execute_script("arguments[0].scrollIntoView(true);", newVideoLinks[399])
                        WebDriverWait(driver, 10)
                        while True:
                            video_count = driver.execute_script("return document.querySelectorAll('ytd-playlist-video-renderer').length;")
                            if video_count > 400:
                                break
                

        new_main = driver.find_element(By.ID,"contents")
        newVideoLinks = new_main.find_elements(By.XPATH, '//*[@id="video-title"]')
        
        video = newVideoLinks[counter]

        video.click()

        driver.implicitly_wait(5)

        data = []
        current_url = driver.current_url

        # Wait for title element
        title_element = driver.find_element(By.XPATH, '//*[@id="title"]/h1/yt-formatted-string')
        title = title_element.text

        # Wait for description elemen

        description_html = driver.find_element(By.XPATH, '//*[@id="description"]')
        
        description_short = description_html.find_element(By.XPATH, '//*[@id="description-inner"]')
        snippet = description_short.find_element(By.ID, "snippet")
        video_player = driver.find_element(By.ID, 'player')
        video_player.click()
        snippet.click()
    

        try:

            description_element = description_html.find_element(By.XPATH, '//*[@id="description-inline-expander"]/yt-attributed-string/span')
            firstdescription = description_element.text

        except Exception as e:

            firstdescription = ''
            

        # Get the text content of title and description
        title = title_element.text
        
        try:
            viewall_button = description_short.find_element(By.XPATH, '//*[@id="navigation-button"]/ytd-button-renderer/yt-button-shape/button')
            viewall_button.click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "contents"))
            )

            chapter_guide = driver.find_element(By.XPATH, '//*[@id="contents"]')
            chapters = chapter_guide.find_elements(By.XPATH, '//*[@id="details"]/h4[1]')

            array_for_unique_chapters = []
            chapters_string = ''
            counter2 = 0
            for chapter in chapters:
                if chapter.text not in array_for_unique_chapters and chapter.text != "":
                    counter2 += 1
                    array_for_unique_chapters.append(chapter.text)
                    if counter2 == 1:
                        chapters_string += chapter.text
                    else:
                        chapters_string += " " + chapter.text
                else:
                    continue

        except Exception as e:
            chapters_string = ""

        description = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Summarize this {firstdescription} and/or this {title} with respect to grammar in one line describing these concepts {chapters_string} or not"},
        ],
        temperature=0,
        )

        data.append({'Title': title, 'Description': description.choices[0].message.content, 'Elements': chapters_string, 'URL': current_url})

        write_to_csv(data)
        
        driver.get("https://www.youtube.com/playlist?list=PL6CQ7apI_8PjSBN8BxukW5Z76k8lRMQEf")

        counter += 1

    driver.quit()
    
    # Append the video data to the list

def write_to_csv(data):
    # Specify the CSV file path
    csv_file_path = 'Grammar.csv'

    # Write the data to the CSV file
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Title', 'Description', 'Elements', 'URL']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the data rows
        writer.writerows(data)

if __name__ == "__main__":
    client = OpenAI(api_key="")
    driver = webdriver.Chrome()  # Change this line based on your browser choice

    # Navigate to YouTube homepage
    driver.get("https://www.youtube.com/playlist?list=PL6CQ7apI_8PjSBN8BxukW5Z76k8lRMQEf")


    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#contents"))
    )

    main = driver.find_element(By.ID,"contents")
    # Find the first few video links on the homepage (you can adjust the range to get more videos)

    video_links = main.find_elements(By.ID,"thumbnail")

    scrape_youtube_data()
