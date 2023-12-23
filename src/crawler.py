import requests
import re
from bs4 import BeautifulSoup

all_output = []

def get_page_content(URL):
    html_text = requests.get(URL).text
    soup = BeautifulSoup(html_text, 'lxml')

    return soup

def parse_raw_text(raw_text):
    cleaned_arabic = ""
    for arabic in raw_text:
        cleaned_arabic += arabic.text.replace('\n', ' ').replace('  ', ' ').replace('×', ' ')

    return cleaned_arabic.strip()

if __name__ == "__main__":

# Put your shamela.ws/book/{NUMBER} link here - without the page number
    
    BOOK_URL = "https://shamela.ws/book/6387"
    current_page = 1

    # Fetch first page of book
    page_content = get_page_content(f'{BOOK_URL}/{current_page}')

    # Find total page count
    final_page_url = page_content.select("a.btn.btn-3d.btn-white.btn-sm")[-1].get('href')
    total_page_count = int(re.search(r'/(\d+)#', final_page_url).group(1))

    print(f"Total pages: {total_page_count}")

    # Loop until the final page is reached
    while current_page <= total_page_count:
        # Find all raw text and parse it
        raw_text = page_content.find_all('div', class_='nass margin-top-10')
        cleaned_arabic = parse_raw_text(raw_text)

        print(f"Page {current_page}:\n{cleaned_arabic}")

        # Add the current page's output to the overall list
        all_output.append({
            'Page': current_page,
            'Content': cleaned_arabic
        })

        # Fetch the next page
        current_page += 1
        page_content = get_page_content(f'{BOOK_URL}/{current_page}#p1')

    # Write the entire output to a single .txt file using utf-8 encoding
    output_file_path = 'all_output.txt'
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for result in all_output:
            output_file.write(f"Page: {result['Page']}\n")
            output_file.write(f"Content:\n{result['Content']}\n\n---\n")

    print(f'\n All output has been written to {output_file_path}')

