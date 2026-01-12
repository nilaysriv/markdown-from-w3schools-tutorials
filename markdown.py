import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import re
import time


START_URL = "https://www.w3schools.com/python/python_dsa_lists.asp" 
BASE_URL = "https://www.w3schools.com"
OUTPUT_DIR = "W3Schools_Python_DSA"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def slugify(text):
    """Convert title to a valid filename for Obsidian."""
    return re.sub(r'[\\/*?:"<>|]', "", text.replace(" ", "_"))

def get_dsa_links():
    """Extracts only the links under the 'Python DSA' heading in the sidebar."""
    print("Fetching tutorial list...")
    response = requests.get(START_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    sidebar = soup.find("div", {"id": "leftmenuinnerinner"})
    if not sidebar:
        print("Error: Could not find the sidebar.")
        return []

    dsa_links = []
    is_dsa_section = False
    
    # Iterate through sidebar elements to find links specifically under the 'Python DSA' header
    for child in sidebar.find_all(['h2', 'a']):
        if child.name == 'h2' and 'Python DSA' in child.text:
            is_dsa_section = True
            continue
        
        # If we hit the next section (like Python MySQL), stop
        if child.name == 'h2' and is_dsa_section:
            break
            
        if is_dsa_section and child.name == 'a':
            href = child.get('href')
            title = child.text.strip()
            # Construct full URL
            full_url = f"{BASE_URL}/python/{href}" if not href.startswith('http') else href
            dsa_links.append((title, full_url))
            
    return dsa_links

def download_page(title, url):
    """Downloads content, converts to markdown, and saves to file."""
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Target the main content area
        main_content = soup.find("div", {"id": "main"})
        if not main_content:
            return

        # Clean up: remove "Previous/Next" buttons and Ad placeholders
        for div in main_content.find_all("div", {"class": ["w3-clear", "nextprev"]}):
            div.decompose()
        for ad in main_content.find_all("div", {"id": "snigel-wrapper"}):
            ad.decompose()

        # Convert to Markdown
        # heading_style="ATX" uses # for headers which is best for Obsidian
        markdown_text = md(str(main_content), heading_style="ATX")
        
        # Post-processing: Remove excessive blank lines
        markdown_text = re.sub(r'\n{3,}', '\n\n', markdown_text)

        # Save file
        filename = f"{slugify(title)}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"--- \ntitle: {title}\nsource: {url}\ntags: [dsa, python, w3schools]\n---\n\n")
            f.write(markdown_text)
            
        print(f"Successfully saved: {filename}")

    except Exception as e:
        print(f"Failed to download {title}: {e}")

def main():
    links = get_dsa_links()
    print(f"Found {len(links)} DSA pages. Starting download...")
    
    for title, url in links:
        download_page(title, url)
        time.sleep(0.5)

    print(f"\nAll done! You can now move the '{OUTPUT_DIR}' folder into your Obsidian vault.")

if __name__ == "__main__":
    main()
