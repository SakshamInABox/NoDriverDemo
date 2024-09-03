import os
import re
import asyncio
import datetime

import nodriver as uc
from bs4 import BeautifulSoup

def screenshot_file_path(page_url):
    # Create Results Folder
    results_folder = "results/" + datetime.datetime.now().strftime('%Y-%m-%d')
    os.makedirs(results_folder, exist_ok=True)

    # Create File Path
    page_url = page_url.split("://")[-1].replace("/", "-")
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    filename = f"[{current_time}]{page_url}.jpeg"
    file_path = os.path.join(results_folder, filename)
    
    return file_path

async def main():
    endpoint = 'https://www.bleepingcomputer.com/'

    # Start New Chrome Instance
    browser = await uc.start()

    # Visit Site & Fetch HTML
    page = await browser.get(endpoint)
    await page.get_content()

    # Locate Class & Extract Content
    elems = await page.select_all('.bc_latest_news_text')
    for elem_object in elems:
        elem = str(elem_object)
        if "london" in elem.lower():
            # Scrape HTML
            soup = BeautifulSoup(elem, 'html.parser')

            # Gather Items
            h4_tag = soup.find('h4')
            title = h4_tag.get_text(strip=True)
            content = soup.find('p').get_text(strip=True)
            link = h4_tag.find('a')['href']

            # Save Screenshot
            page = await browser.get(link)
            await page.save_screenshot(filename=screenshot_file_path(link))
            
            print("H4 Content:", content)
            print("H4 Link:", link)
            print("Paragraph Content:", content)

            #Do Whatever Here - Send to Discord/Slack/Telegram

    # Close Page
    await page.close()
    
if __name__ == '__main__':
    uc.loop().run_until_complete(main())
