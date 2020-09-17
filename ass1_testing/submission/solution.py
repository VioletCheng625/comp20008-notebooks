# Task 1
# Extracts articles from a given website
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

url = 'http://comp20008-jh.eng.unimelb.edu.au:9889/main/'
headlines = []
urls = []
# Store unvisited links
to_visit = []
visited = {}; 
visited[url] = True

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
# Resolve to absolute urls
next_url = urljoin(url, soup.find('a')['href'])
to_visit.append(next_url)
urls.append(next_url)

# Find all outbound links on succsesor pages and explore each one
while (to_visit):
    link = to_visit.pop(0)
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Mark the item as visited, i.e., add to visited list, remove from to_visit
    visited[link] = True
    new_link = soup.findAll('a')[1]
    new_url = urljoin(url, new_link['href'])
    to_visit.append(new_url)
    headlines.append(soup.find('h1').string)
    
    # Stop when all links have been visited
    if new_url in visited:
        break
    
    urls.append(new_url)
    
# Construct csv file    
table = csv.writer(open('task1.csv', 'w'))
table.writerow(['url', 'headline'])
for i in range(len(urls)):
    table.writerow([urls[i], headlines[i]])
    
    
    
 # Task 2
# a)
# Extract the name of the first team mentioned in the article
# b)
# Extract the largest match score
import json
import re

# Turn the JSON object into a Python dictionary
with open('rugby.json', 'r') as rugby:
    diction = json.load(rugby)

# List of first team in the article
team = []
new_urls = []
new_headlines = []
max_score = []

# Do iterative search in the dictionaty for the team name
# If found, add elements to the new lists
for i in range(1, len(urls)):
    page = requests.get(urls[i])
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Combine the headline and the main article on each page
    content = soup.find('h1').string
    piece = soup.findAll('p')
    for k in range(len(piece)):
        content = content + piece[k].string
    
    # Ensure the match position index is the minimum
    pos = float("inf")
    match = False
    for j in range(len(diction['teams'])):
        word = diction['teams'][j]['name']
        # Extract all match scores on each page
        scores = re.findall(r"\d+-\d+", content)
        
        # Discard if no team match or no score match
        if re.search(word, content) and scores != []:
            match = True
            max_val = 0
            for score in scores:
                score1 = int(re.findall(r"\d+", score)[0])
                score2 = int(re.findall(r"\d+", score)[1])
                # Assume the score is always below 100-100
                if score1+score2 < 200 and score1+score2 > max_val:
                    max_val = score1 + score2
                    max_toString = str(score1) + '-' + str(score2)
            # Avoid repeatedly recording
            if urls[i] not in new_urls:
                new_urls.append(urls[i])
                new_headlines.append(headlines[i])
                max_score.append(max_toString)
            # Update minimum match position index
            if re.search(word, content).span()[0] < pos:
                pos = re.search(word, content).span()[0]
                name = word
    if match:
        team.append(name)
        
# Construct csv file    
table = csv.writer(open('task2.csv', 'w'))
table.writerow(['url', 'headline', 'team', 'score'])
for i in range(len(new_urls)):
    table.writerow([new_urls[i], new_headlines[i], team[i], max_score[i]])


# Task 3
# Average game difference of each team mentioned
team_mentioned = []
average_difference = []
team_mentioned.append(team[0])
# Get a list of teams mentioned
for i in range(len(team)):
    if team[i] not in team_mentioned:
        team_mentioned.append(team[i])

times_mentioned = [0] * len(team_mentioned)
game_difference = [0] * len(team_mentioned)
# Calculate total difference and total times of each team mentioned
for i in range(len(team_mentioned)):
    for j in range(len(team)):
        if team_mentioned[i] == team[j]:
            times_mentioned[i] = times_mentioned[i] + 1;
            match_score = max_score[j]
            score1 = int(re.findall(r"\d+", match_score)[0])
            score2 = int(re.findall(r"\d+", match_score)[1])
            game_difference[i] = game_difference[i] + abs(score1 - score2)

# Using division to calculate the average
for i in range(len(game_difference)):
    average_difference.append(float(game_difference[i]) / times_mentioned[i])
    
# Construct csv file    
table = csv.writer(open('task3.csv', 'w'))
table.writerow(['team', 'avg_game_difference'])
for i in range(len(team_mentioned)):
    table.writerow([team_mentioned[i], average_difference[i]])
    




# Task 4
# Generate a plot of five teams
import matplotlib.pyplot as plt
times_mentioned_temp = []
# Copy times_mentioned
for i in range(len(times_mentioned)):
    times_mentioned_temp.append(times_mentioned[i])

max_times = []
max_teams = []
for i in range(5):
    max_val = max(times_mentioned_temp)
    max_times.append(max_val)
    times_mentioned_temp.remove(max_val)
    max_teams.append(team_mentioned[times_mentioned.index(max_val)])

plt.bar(max_teams, max_times)
plt.ylabel('Times Mentioned')
plt.xlabel('Teams Mentioned')
plt.title("Top 5 Teams Mentioned")
plt.savefig('task4.png')




# Task 5
# Generate a plot comparing times mentioned and average game difference
plt.scatter(times_mentioned, average_difference)
plt.ylabel('Average Game Difference')
plt.xlabel('Times Mentioned in Articles')
plt.title("Times Mentioned vs Average Game Difference")
for i in range(len(times_mentioned)):
    plt.annotate(team_mentioned[i], (times_mentioned[i], average_difference[i]))
plt.savefig('task5.png')
