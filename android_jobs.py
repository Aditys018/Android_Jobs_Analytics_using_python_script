import requests
from bs4 import BeautifulSoup
import random
import time
import matplotlib.pyplot as plt


url = 'https://www.linkedin.com/jobs/search/?keywords=Android%20Developer'

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36'
]

job_counts = {}


for page in range(1, 3):  
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    response = requests.get(f"{url}&start={page*25}", headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        jobs = soup.find_all('div', class_='base-search-card__info')

        for job in jobs:
            job_title = job.find('h3', class_='base-search-card__title').get_text(strip=True)
            job_counts[job_title] = job_counts.get(job_title, 0) + 1

        time.sleep(2)  
    elif response.status_code == 429:
        print("Rate limit exceeded. Waiting before retrying...")
        time.sleep(60)
    else:
        print(f"Request failed with status code: {response.status_code}")


job_counts_short = {k: v for k, v in sorted(job_counts.items(), key=lambda item: item[1], reverse=True)[:6]}
job_titles = list(job_counts_short.keys())
job_values = list(job_counts_short.values())


plt.figure(figsize=(15, 10), facecolor='black')
plt.style.use('dark_background')

# Pie Chart
plt.subplot(3, 1, 1)  # 3 rows, 1 column, 1st subplot
wedges, texts, autotexts = plt.pie(
    job_values, 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=plt.cm.tab10.colors,
    wedgeprops=dict(linewidth=2, edgecolor='black')
)
plt.title('Job Title Distribution for Android Developer Positions', fontsize=16)
plt.axis('equal') 

# Bar Graph
plt.subplot(3, 1, 2) 
plt.barh(job_titles, job_values, color=plt.cm.tab10.colors)
plt.title('Job Count for Android Developer Positions', fontsize=16)
plt.xlabel('Count', fontsize=14)
plt.grid(axis='x', color='gray', linestyle='--', linewidth=0.5)

# Line Graph 
years = ['2020', '2021', '2022', '2023', '2024']
dummy_data = [10, 20, 30, 25, 40] 
plt.subplot(3, 1, 3) 
plt.plot(years, dummy_data, marker='o', color='cyan')
plt.title('Trend of Android Developer Jobs Over Years', fontsize=16)
plt.ylabel('Job Count', fontsize=14)
plt.grid(True)


plt.tight_layout()
plt.show()
