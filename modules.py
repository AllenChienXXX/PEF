def get_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # extract all the texts
    all_text = soup.get_text()
    all_text = re.sub(r"\s+", " ", all_text)
    # print(all_text)
    return all_text
# get text content type from email
def get_text(file_path):
    with open(file_path, 'rb') as file:
        message = email.message_from_bytes(file.read())
        text_content = ""
        for part in message.walk():
            if part.get_content_type() == 'text/plain':
                text_content += part.get_payload(decode=True).decode('iso-8859-1')
                # print(text_content)
                return text_content.replace("\n","")
        if text_content == "":
            return get_text_from_html(get_html_general(file_path));
from bs4 import BeautifulSoup
import email
def get_email_html(file_path):
    with open(file_path, 'rb') as file:
        content = email.message_from_bytes(file.read())
        html_content = ""
        for part in content.walk():
            if part.get_content_type() == 'text/html':
                html_content += part.get_payload(decode=True).decode('iso-8859-1')
        html_content.replace("\n","")
        if html_content != "":
            # print("Found html at "+file_path)
            return html_content
        else:
            # print("No html content found at "+file_path)
            return ""

#get html by searching for <html> tag
def get_html(file_path):
    with open(file_path, 'r',encoding='iso-8859-1') as file:
        html_flag = False
        html_content = "";
        tag_list = []
        for line in file:
            words = line.split()
            for word in words:
                if word == "<html>":
                    html_flag = True;
                if html_flag:
                    html_content += word
                if word == "</html>":
                    html_flag = False;
        # print(html_content)
        html_content.replace("\n","")
        if html_content == "":
            # print("No html content found at "+file_path)
            return ""
        else:
            # print("Found html at "+file_path)
            return html_content

def get_html_general(file_path):
    if get_email_html(file_path)!="":
        return get_email_html(file_path)
    else:
        return get_html(file_path)
def get_onclicks(file_path):
    content = get_html_general(file_path)
    if content == "": return None
    soup = BeautifulSoup(content, 'html.parser')

    elements = soup.find_all(attrs={'onClick': True})
    # Count the number of elements with an onClick attribute
    count = len(elements)
    return count
def check_popWindow(file_path):
    content = get_html_general(file_path)
    if content == "": return None
    soup = BeautifulSoup(content, 'html.parser')

    # Check if any <script> tags were found
    try:
        scripts = soup.find_all('script', text=lambda text: 'window.open' in text)
        if scripts:
            return True
            # print('The email body contains a script that attempts to modify the status bar.')
        else:
            # print('The email body does not contain a script that attempts to modify the status bar.')
            return False
    except TypeError:
        return False

def check_spf(file_path):
  with open(file_path, 'rb') as file:
    message = email.message_from_bytes(file.read())
    received_spf_header = message.get('Received-SPF')
    if received_spf_header == None:
      return 0
    if received_spf_header:
        spf_result = received_spf_header.split()[0].lower()
        if spf_result == 'pass':
          return 1
        elif spf_result == 'neutral':
          return 2
        elif spf_result == 'softfail':
          return 3
        else:
          return 0
    else:
        return 0
def check_dkim(file_path):
  with open(file_path, 'rb') as file:
    message = email.message_from_bytes(file.read())
    auth = message.get('Authentication-Results')
    if auth == None:
      return 0
    auth_result = auth.split()
    # print(auth)
    # print(dkim_result)
    if 'dkim=pass' in auth_result:
      return 1
    else:
      return 0
def check_dmarc(file_path):
  with open(file_path, 'rb') as file:
    message = email.message_from_bytes(file.read())
    auth = message.get('Authentication-Results')
    if auth == None:
      return 0
    auth_result = auth.split()
    # print(auth)
    # print(dkim_result)
    if 'dmarc=pass' in auth_result:
      return 1
    else:
      return 0
def check_deliver_receiver(filepath):
  with open(filepath, 'rb') as file:
    message = email.message_from_bytes(file.read())
    deliver = message.get('Delivered-To')
    # print(deliver)
    receiver = message.get('To')
    # print(receiver)
    if deliver == receiver:
      return 1
    else:
      return 0
def check_encript(filepath):
  with open(filepath, 'rb') as file:
    message = email.message_from_bytes(file.read())
    received_headers = message.get_all('Received')
    # print(received_headers)
    version_string = 'version'
    try:
      for received_header in received_headers:
          if version_string in received_header:
              return 1
    except TypeError:
      return 0
    return 0
def get_tags_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    tag_list = []
    html_tags = soup.find_all()
    for tag in html_tags:
        tag_list += [tag.name]
    # print(tag_list)
    return tag_list
import ipaddress
from urllib.parse import urlparse
import urllib.request
from bs4 import BeautifulSoup
import re
import email

#get urls in html content
def get_urls_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    urls = []
    # get all the urls
    anchor_tags = soup.find_all('a')
    for tag in anchor_tags:
        href = tag.get('href')
        if href:
            if re.match('^https?://', href):
                # print(href)
                urls += [href]
    return urls
def get_text(file_path):
    with open(file_path, 'rb') as file:
        message = email.message_from_bytes(file.read())
        text_content = ""
        for part in message.walk():
            if part.get_content_type() == 'text/plain':
                text_content += part.get_payload(decode=True).decode('iso-8859-1')
                # print(text_content)
                return text_content.replace("\n","")
        if text_content == "":
            return get_text_from_html(get_html_general(file_path));
def get_num_words(file_path):
    if get_text(file_path) != "":
        words = len(get_text(file_path).split())
        return words
    if get_html_general(file_path) != "":
        words = len(get_text_from_html(get_html_general(file_path)).split())
        return words
    else:
        return 0

# get how many characters in the email text or html
def get_num_chars(file_path):
    if get_text(file_path) != "":
        chars = len(get_text(file_path).replace(" ",""))
        return chars
    if get_html_general(file_path) != "":
        chars = len(get_text_from_html(get_html_general(file_path)).replace(" ",""))
        return chars
    else:
        return 0

#calculate the body richness by dividing number of words with number of characters
def get_body_richness(filepath):
    if get_num_chars(filepath) == 0: return 0
    return get_num_words(filepath)/get_num_chars(filepath)

#get how many function words is in the content
def get_num_FunctionWords(file_path):
    function_words = ["account","access","bank","credit","click","identity","inconvenience","information","limited","log","minutes","password","recently","risk","social","security","service","suspended"]
    content = ""
    count = 0
    if get_text(file_path) != "":
        content = get_text(file_path).split()
    elif get_html_general(file_path) != "":
        content = get_text_from_html(get_html_general(file_path)).split()
    else:
        return None
    for w in function_words:
        if w in content:
            count += 1
    return count


def get_email_html(file_path):
    with open(file_path, 'rb') as file:
        content = email.message_from_bytes(file.read())
        html_content = ""
        for part in content.walk():
            if part.get_content_type() == 'text/html':
                html_content += part.get_payload(decode=True).decode('iso-8859-1')
        html_content.replace("\n","")
        if html_content != "":
            # print("Found html at "+file_path)
            return html_content
        else:
            # print("No html content found at "+file_path)
            return ""

#get how many words in subject
def get_num_sbj(file_path):
    count = len(get_subject(file_path).split())
    return count
def get_subject(file_path):
    with open(file_path, 'rb') as file:
        message = email.message_from_bytes(file.read())
        headers = message.items()
        # Print the headers
        subject = ""
        for header in headers:
            if header[0] == "Subject":
                # print(header[1])
                subject = header[1]
                break
        # if subject == "":
            # print("No subject found")
        subject = re.sub(r"\s+", " ", str(subject))
        return subject


def get_sender(file_path):
    with open(file_path, 'rb') as file:
        message = email.message_from_bytes(file.read())
        headers = message.items()
        # Print the headers
        sender = ""
        for header in headers:
            if header[0] == "From":
                # print(header[1])
                sender = header[1]
                break
        if sender == "":
            return None
        # subject = re.sub(r"\s+", " ", str(subject))
        return sender

#get how many characters in subject
def get_num_sbjChar(file_path):
    count = len(get_subject(file_path))
    return count

#claculate the subject richness by dividing words with characters
def get_sbj_richness(file_path):
    if get_num_sbjChar(file_path) == 0:return 0
    return get_num_sbj(file_path)/get_num_sbjChar(file_path)

# get how many urls have ip address in it
def get_num_urls_ip(file_path):
    content = get_html_general(file_path)
    if content == "": return 0
    urls = get_urls_from_html(content)
    num_ip = 0
    for url in urls:
        from urllib.parse import urlparse
        hostname = urlparse(url).hostname
        try:
            ip_address = ipaddress.ip_address(hostname)
            num_ip+=1
            # print(f"{url} contains an IP address: {ip_address}")
        except ValueError:
            pass
            # print(f"{url} does not contain an IP address")

    return num_ip

# return the total amount of urls in html content
def get_num_urls(file_path):
    urls = get_urls_from_html(get_html_general(file_path))
    if urls == []:
        return None
    return len(urls)

# get how many image urls in the html
def get_num_image_urls(file_path):
    soup = BeautifulSoup(get_html_general(file_path), 'html.parser')

    # Find all <a> tags that contain an <img> tag
    image_links = soup.find_all('a', href=True, recursive=True, limit=None, string=None)
    image_links_with_img = [link for link in image_links if link.find('img')]
    return len(image_links_with_img)
    # Extract the href and src attributes of each image link
    # for link in image_links_with_img:
    #     href = link['href']
    #     src = link.find('img')['src']
    #     print(f"Clickable image link: {href} - Image URL: {src}")

# get numbers of urls contain domain name
def get_num_domain_urls(file_path):
    urls = get_urls_from_html(get_html_general(file_path))
    domains = set()
    for url in urls:
        match = re.search(r'https?://([^/]+)/', url)
        if match:
            domain = match.group(1)
            domains.add(domain)

    # Count the number of domains in the set and print the result
    num_domains = len(domains)
    return num_domains


#get how many urls contain port info
def get_num_url_ports(file_path):
    urls = get_urls_from_html(get_html_general(file_path))
    count = 0
    for url in urls:
        parsed_url = urlparse(url)
        # Check if the parsed URL includes a port number
        if parsed_url.port:
            count += 1
        #     print(f'The URL "{url}" contains port {parsed_url.port}')
        # else:
        #     print(f'The URL "{url}" does not contain a port')
    return count


#get how many characters in sender
def get_chars_sender(file_path):
    sender = get_sender(file_path)
    return len(str(sender))