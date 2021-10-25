import requests
import pandas as pd
from bs4 import BeautifulSoup



# r = requests.get('https://www.shudder.com/movies')
# data = r.text
data = open('DS.html', 'r')
soup = BeautifulSoup(data, features='html.parser')
titles = []

movies = soup.find_all('h5', attrs={'class': 'headline sm up'})
for movie in movies:
    title = str(movie.find(text=True, recursive=False))
    camel_case_title = title.replace(' ', '_').lower()
    titles.append({
        'title': title,
        'cc_title': camel_case_title
    })


audience_score = []
critics_score = []
film_titles = []
for title in titles:
    r = requests.get(f'https://www.rottentomatoes.com/m/{title["cc_title"]}')
    data = r.text
    soup = BeautifulSoup(data, features='html.parser')
    scoreboard = soup.find_all('score-board')
    for score in scoreboard:

        audience_score.append(score['audiencescore'])
        critics_score.append(score['tomatometerscore'])
        film_titles.append(title['title'])
        print(f'Title: {title["title"]}, Critics: {score["tomatometerscore"]}, Audience {score["audiencescore"]}')

film_scores = pd.DataFrame({"Title": film_titles, "Critic's Score": critics_score, "Audience Score": audience_score})

film_scores["Critic's Score"] = pd.to_numeric(film_scores["Critic's Score"])
film_scores["Audience Score"] = pd.to_numeric(film_scores["Audience Score"])
film_scores = film_scores.sort_values(by=["Critic's Score"], ascending=False)

film_scores.style.set_properties(subset=["Critic's Score"], **{'width': '400px'})

film_scores.reset_index(drop=True, inplace=True)
film_scores.index = film_scores.index + 1

print(film_scores)
film_scores.to_csv('shudder_films_ranked.csv', na_rep='N/A')