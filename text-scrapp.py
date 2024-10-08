#import what we need
from requests_html import HTMLSession

# Initialize session
session = HTMLSession()

# Use session to get the page
r = session.get('https://www.kompas.com/')

# Render the HTML, sleep=1 to ensure page load, scrolldown to get more content
r.html.render(sleep=1, scrolldown=5)

# Find all articles using inspect element and create a blank list
articles = r.html.find('article')
newslist = []

# Loop through each article to find the title and link
for item in articles:
    try:
        newsitem = item.find('h4', first=True)  # Assuming h4 is used for article titles
        title = newsitem.text
        link = list(newsitem.absolute_links)[0]  # Convert absolute_links to list and extract the first item
        newsarticle = {
            'title': title,
            'link': link
        }
        newslist.append(newsarticle)
    except Exception as e:
        print(f"Error occurred: {e}")
        pass

# Save the news articles to a file 'new.txt'
with open('new.txt', 'w', encoding='utf-8') as f:
    for news in newslist:
        f.write(f"Title: {news['title']}\n")
        f.write(f"Link: {news['link']}\n\n")

# Print the number of articles found
print(f"Number of articles found: {len(newslist)}")
