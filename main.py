#ParamSan
import argparse
import requests
import time
import os
import platform
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def clear_screen():
    # Mendeteksi sistem operasi
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def extract_urls_with_parameters(url, proxy=None, timeout=None):
    session = requests.Session()
    if proxy:
        session.proxies = {'http': proxy, 'https': proxy}
    
    try:
        response = session.get(url, timeout=timeout)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            urls_with_parameters = []
            for link in links:
                href = link['href']
                parsed_url = urlparse(href)
                query_params = parsed_url.query
                if query_params:
                    urls_with_parameters.append(href)
            
            return urls_with_parameters
        else:
            print(f"Failed to fetch URL: {response.status_code}")
    except requests.Timeout:
        print("Connection timeout occurred.")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def process_urls(urls, output_file=None, proxy=None, timeout=None, sleep=None):
    extracted_urls = []
    for url in urls:
        url = url.strip()
        print(f" Start URL - {url}")
        urls_with_parameters = extract_urls_with_parameters(url, proxy, timeout)
        if urls_with_parameters:
            for url_with_parameters in urls_with_parameters:
                extracted_url = url + "/" + url_with_parameters
                extracted_urls.append(extracted_url)
                if output_file:
                    with open(output_file, 'a') as file:
                        file.write(extracted_url + '\n')
                else:
                    print(extracted_url)
            if sleep:
                time.sleep(sleep)

def print_banner():
    banner = """
 ____                           ____              
|  _ \ __ _ _ __ __ _ _ __ ___ / ___|  __ _ _ __  
| |_) / _` | '__/ _` | '_ ` _ \|___ \ / _` | '_ \ 
|  __/ (_| | | | (_| | | | | | |___) | (_| | | | |
|_|   \__,_|_|  \__,_|_| |_| |_|____/ \__,_|_| |_|
                                    x-projetion.github.io

"""
    print(banner)

if __name__ == "__main__":
    clear_screen()
    print_banner()
    parser = argparse.ArgumentParser(description="ParamSan is a fast crawler that focuses on retrieving url parameters from a given url")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--url", help="URL to extract URLs with parameters from")
    group.add_argument("-l", "--list", help="File containing list of URLs")
    parser.add_argument("-o", "--output", help="Output file to save extracted URLs")
    parser.add_argument("-p", "--proxy", help="Proxy to use for making requests (e.g., http://proxy:port)")
    parser.add_argument("-t", "--timeout", type=float, help="Timeout for making HTTP requests")
    parser.add_argument("-s", "--sleep", type=float, help="Sleep duration between requests")
    args = parser.parse_args()

    if args.url:
        process_urls([args.url], args.output, args.proxy, args.timeout, args.sleep)
    else:
        try:
            with open(args.list, 'r') as file:
                urls = file.readlines()
                process_urls(urls, args.output, args.proxy, args.timeout, args.sleep)
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print("An error occurred:", str(e))
