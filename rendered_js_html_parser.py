from bs4 import BeautifulSoup
import requests
import os

def get_webpage(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_resources(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')

    # Extract and replace the links in <style> tags
    for style in soup.find_all('link', {'rel': 'stylesheet'}):
        href = style.get('href')
        if href and not href.startswith(('http:', 'https:')):
            href = base_url + href
        style['href'] = href

    # Extract and replace the links in <script> tags
    for script in soup.find_all('script', {'src': True}):
        src = script['src']
        if src and not src.startswith(('http:', 'https:')):
            src = base_url + src
        script['src'] = src


    return soup.prettify()

def main():
    url = "https://dbd.go.th/"  # Replace with the desired URL
    base_url = "{0.scheme}://{0.netloc}".format(requests.utils.urlparse(url))
    html = get_webpage(url)
    modified_html = extract_resources(html, base_url)

    # Initialize the base filename and counter
    base_filename = 'modified_page'
    file_extension = '.html'
    counter = 0

    # Construct the initial filename
    filename = f"{base_filename}{file_extension}"

    # Loop to find a filename that doesn't exist
    while os.path.exists(filename):
        counter += 1
        filename = f"{base_filename}[{counter}]{file_extension}"

    # Write the content to the new file
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(modified_html)

if __name__ == '__main__':
    main()
