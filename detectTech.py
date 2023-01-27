import csv
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


def detect_tech(url):
    try:
        ua = UserAgent()
        headers = {'User-Agent': ua.random, 'Cache-Control': 'no-cache'}
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=5)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = session.get(url, allow_redirects=True, headers=headers)
        url = response.url
        print(url)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        technologies = {
            'Hubspot': False,
            'Zoho': False,
            'WordPress': False,
            'Webflow': False,
            'Mautic': False,
            'Salesforce': False
        }
        scripts = soup.find_all('script')
        for script in scripts:
            src = script.get('src', '')
            text = script.text
            if 'salesforce.com' in src or 'salesforce.com' in text:
                technologies['Salesforce'] = True
            if 'hs-analytics' in src or '_hsq' in text :
                technologies['Hubspot'] = True
            if 'hs-scripts' in src :
                technologies['Hubspot'] = True
            if 'hsforms' in src or 'hsforms' in text:
                technologies['Hubspot'] = True
            if 'zohomodules' in src or 'zohomodules' in text:
                technologies['Zoho'] = True
            if 'pagesense.io' in src or 'zoho' in text:
                technologies['Zoho'] = True
            if 'wp-content' in src or 'wp-content' in text:
                technologies['WordPress'] = True
            if 'webflow' in src or 'webflow' in text:
                technologies['Webflow'] = True
            if 'mautic' in src or 'mautic' in text:
                technologies['Mautic'] = True

        links = soup.find_all('link')
        for link in links:
            href = link.get('href', '')
            if 'hs-analytics' in href:
                technologies['Hubspot'] = True
            if 'zohomodules' in href:
                technologies['Zoho'] = True
            if 'wp-content' in href:
                technologies['WordPress'] = True
            if 'webflow' in href:
                technologies['Webflow'] = True
            if 'mautic' in href:
                technologies['Mautic'] = True
        return technologies
    except requests.exceptions.RequestException as e:
        print(f"Error {e} for {url}")
        return None

# Open the input CSV file
with open('websites.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip the header row

    # Open the output CSV file
    with open('results.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        # Iterate over the URLs
        for row in reader:
            url = row[0]
            if not url.startswith("http"):
                url = "http://" + url
            try:
                # Get the website technologies
                technologies = detect_tech(url)
                technologies_list = []
                if technologies == "Error":
                    technologies_list = ["Error"] * len(technologies.keys())
                else:
                    if technologies['Hubspot']:
                        technologies_list.append("Hubspot")
                    else:
                        technologies_list.append("-")
                    if technologies['Zoho']:
                        technologies_list.append("Zoho")
                    else:
                        technologies_list.append("-")
                    if technologies['WordPress']:
                        technologies_list.append("WordPress")
                    else:
                        technologies_list.append("-")
                    if technologies['Webflow']:
                        technologies_list.append("Webflow")
                    else:
                        technologies_list.append("-")
                    if technologies['Mautic']:
                        technologies_list.append("Mautic")
                    else:
                        technologies_list.append("-")
                    if technologies['Salesforce']:
                        technologies_list.append("Salesforce")
                    else:
                        technologies_list.append("-")

                print(f"{technologies} !Done")
            
                # Write the results to the output CSV file
                writer.writerow([url, technologies_list[0], technologies_list[1],
                                technologies_list[2], technologies_list[3], technologies_list[4]])
                print("!!Written")

            except Exception as e:
                print(f"Error {e} for {url}")
                continue
        print("All Done, Check CSV Result Now")

