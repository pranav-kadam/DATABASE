import requests
from bs4 import BeautifulSoup
import re
from openpyxl import Workbook

def extract_webpage_data(link):
    response = requests.get(link)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the webpage. Status code: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')

    profiles = soup.find_all('div', class_='mini-profile')
    data = []

    for profile in profiles:
        name = profile.find('h4')
        name = name.text.strip() if name else None

        course = profile.find('h5')
        course = course.text.strip() if course else None

        email_div = profile.find('div', class_='extra-bottom-padding')
        email = None
        if email_div:
            email_link = email_div.find('a', href=lambda href: href and href.startswith('mailto:'))
            if email_link:
                email = email_link.text.strip()

        if name or course or email:
            data.append((name, course, email))

    return data

def save_to_excel(all_data):
    wb = Workbook()
    ws = wb.active
    ws.title = "Stanford Profile Data"
    
    headers = ["Name", "Course", "Email"]
    ws.append(headers)
    
    for sheet_number, data in enumerate(all_data, start=1):
        ws = wb.create_sheet(title=f"Page {sheet_number}")
        ws.append(headers)
        for row in data:
            ws.append(row)
    
    wb.save("stanford_profile_data.xlsx")
    print("Data saved to stanford_profile_data.xlsx")

def main():
    base_url = "https://profiles.stanford.edu/browse/school-of-engineering?p={}&ps=100"
    all_data = []

    for i in range(1, 65):
        link = base_url.format(i)
        try:
            data = extract_webpage_data(link)
            all_data.append(data)
            print(f"Extracted data from page {i}")
        except Exception as e:
            print(f"An error occurred on page {i}: {str(e)}")

    save_to_excel(all_data)

if __name__ == "__main__":
    main()
