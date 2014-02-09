import urllib2

url = raw_input("Enter the website: ")

response = urllib2.urlopen(url)
html = response.read()

def get_title(html):
    html_lowered = html.lower();
    begin = html_lowered.find('<title>')
    end = html_lowered.find('</title>')
    if begin == -1 or end == -1:
        return None
    else:
        return html[begin+len('<title>'):end].strip()

title = get_title(html)

print title

response.close()
