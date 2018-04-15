import requests
import json
from bs4 import BeautifulSoup
import sys
import codecs
import sqlite3
import csv
from secrets import *
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
#NEED VIRTUAL ENVIRONMENT - SEE LECTURE 23
#re-generate your requirements.txt as a final step before submitting your project. Just in case.

#Caching for TMDB data:
try:
    cache_file = open('cache_tmdb.json', 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

def make_request_using_cache(url, params):
    unique_ident = params_unique_combination(url, params)
    if unique_ident in CACHE_DICTION:
        print("Getting cached data for TMDB data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new TMDB data...")
        resp = requests.get(url, params = params)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open('cache_tmdb.json',"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

#Getting API key from secrets.py:
TMDB_API_KEY = api_key

#Function for getting data from TMDB Api:
def get_tmdb_data():
    top_2016_movies = []

    url = "https://api.themoviedb.org/3/discover/movie"

    response_page_1 = make_request_using_cache(url, params={'api_key': TMDB_API_KEY, 'region': 'US', 'sort_by': 'popularity.desc', 'page': 1, 'primary_release_year': 2016})
    response_page_2 = make_request_using_cache(url, params={'api_key': TMDB_API_KEY, 'region': 'US', 'sort_by': 'popularity.desc', 'page': 2, 'primary_release_year': 2016})
    response_page_3 = make_request_using_cache(url, params={'api_key': TMDB_API_KEY, 'region': 'US', 'sort_by': 'popularity.desc', 'page': 3, 'primary_release_year': 2016})
    response_page_4 = make_request_using_cache(url, params={'api_key': TMDB_API_KEY, 'region': 'US', 'sort_by': 'popularity.desc', 'page': 4, 'primary_release_year': 2016})
    response_page_5 = make_request_using_cache(url, params={'api_key': TMDB_API_KEY, 'region': 'US', 'sort_by': 'popularity.desc', 'page': 5, 'primary_release_year': 2016})

    top_2016_movies.append(response_page_1)
    top_2016_movies.append(response_page_2)
    top_2016_movies.append(response_page_3)
    top_2016_movies.append(response_page_4)
    top_2016_movies.append(response_page_5)
    #print(top_2016_movies)

#get_tmdb_data()



#Scraping:
try:
    cache_file = open("cache_halloween.json", 'r')
    cache_contents = cache_file.read()
    CACHE_HTML = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_HTML = {}

def make_scrape_request_using_cache(url):
    unique_ident = url
    if unique_ident in CACHE_HTML:
        print("Getting cached data for halloween costumes...")
        return CACHE_HTML[unique_ident]
    else:
        print("Making a request for new data for halloween costumes...")
        resp = requests.get(url)
        CACHE_HTML[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_HTML)
        fw = open("cache_halloween.json", "w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_HTML[unique_ident]

#Class:
class HalloweenCostumes:
    def __init__(self, header="No header", costume_name="no costume name"):
        self.header = header
        self.costume_name = costume_name

def scrape_halloween_costumes():
    header_list = []
    costume_list = []

    new_list = []

    base_url = "https://nrf.com/media/press-releases/trading-crowns-capes-superhero-is-top-choice-halloween"
    main_page_text = make_scrape_request_using_cache(base_url)
    main_page_soup = BeautifulSoup(main_page_text, 'html.parser')
    content_div = main_page_soup.find_all('div', class_='field field-name-field-db-paragraph field-type-text-long field-label-hidden')

    with open('costumes.csv', 'w') as csvDataFile:
        my_writer = csv.writer(csvDataFile)

        for x in content_div:
            all_headers = x.find_all("h3") #list of h3 tags
            header_text = ""
            costume_text = ""

            for header in all_headers:
                try:
                    header_text = header.text
                except:
                    pass

            all_costumes = x.find_all("li") #list of costumes
            for costume in all_costumes:
                try:
                    costume_text = costume.text
                except:
                    pass
                my_writer.writerow((costume_text,header_text))

            #course = [header_text, costume_text]
        # new_list.append(header_list)
        # new_list.append(costume_list)
        # print(new_list)
        #
        # for row in new_list:
        #     my_writer.writerow(row)


        #my_writer.writerow("Costume Name, Age Group")
        #
        # for val in costume_list:
        #     my_writer.writerow([val])
        #
        # for val in header_list:
        #     my_writer.writerow([val])

        #my_writer.writerow(header_list)
        #my_writer.writerow(costume_list)

    #costume = HalloweenCostumes(header=all_headers, costume_name=all_costumes)

#scrape_halloween_costumes()

#Reading data into new database:
def init_db():
    DBNAME = 'movies.db'
    print('Creating Database')
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except:
        print("Error with db")

    #For JSON file:
    statement_json = ''' DROP TABLE IF EXISTS 'Movies'; '''
    cur.execute(statement_json)
    conn.commit()

    statement_json = '''
        CREATE TABLE 'Movies' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'VoteAverage' TEXT NOT NULL,
        'Title' TEXT NOT NULL,
        'Popularity' TEXT NOT NULL,
        'VoteCount' Integer NOT NULL,
        'Overview' TEXT NOT NULL,
        'ReleaseDate' TEXT NOT NULL
         );
     '''
    cur.execute(statement_json)
    conn.commit()

    #For CSV file (scraping):
    statement_csv = ''' DROP TABLE IF EXISTS 'Costumes'; '''
    cur.execute(statement_csv)
    conn.commit()

    #AGEGROUPID WILL PULL FROM AGE GROUP TABLE
    statement_csv = '''
        CREATE TABLE 'Costumes' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'CostumeName' TEXT NOT NULL,
        'AgeGroupId' TEXT NOT NULL
         );
     '''
    cur.execute(statement_csv)
    conn.commit()

    #For age group table:
    statement_age_group = ''' DROP TABLE IF EXISTS 'AgeGroup'; '''
    cur.execute(statement_age_group)
    conn.commit()

    statement_age_group = '''
        CREATE TABLE 'AgeGroup' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'GroupName' TEXT NOT NULL
         );
     '''
    cur.execute(statement_age_group)
    conn.commit()

    conn.close()


#Inserting JSOn data:
def insert_json_data():
    TMDBJSON = 'cache_tmdb.json'
    try:
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
    except:
        print("Error inserting json data")

    print("Inserting json data")

    #Opening JSON file:
    str_file = open(TMDBJSON, 'r', encoding="utf8")
    content = str_file.read()
    movies_dict = json.loads(content)

    for url, movies in movies_dict.items():
        movie_dict2 = json.loads(movies)
        results = movie_dict2["results"]
        for movie in results:
            #print(movie["title"])
            #print("------------------------------")
            insertion = (None, movie['vote_average'], movie['title'], movie['popularity'], int(movie['vote_count']), movie['overview'], movie['release_date'])
            statement_json = 'INSERT INTO "Movies" '
            statement_json += 'VALUES (?, ?, ?, ?, ?, ?, ?) '
            cur.execute(statement_json, insertion)
    conn.commit()
    conn.close()


#Inserting CSV data into age group table:
def insert_age_group_data():
    COSTUMES_CSV = 'costumes.csv'
    try:
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
    except:
        print("Error inserting age group data")

    print("Inserting age group data")

    costume_age_groups = ["Children's Costumes", "Adults 18-34-years-old", "Adults 35+", "Pets"]

    for age in costume_age_groups:
        insertion = (None, age)
        statement = 'INSERT INTO "AgeGroup" '
        statement += 'VALUES (?, ?) '
        cur.execute(statement, insertion)
        conn.commit()
    conn.close()


#Inserting data into Costumes table:
def insert_csv_data():
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    query = "SELECT * FROM AgeGroup"
    cur.execute(query)

    costume_mapping = {}
    for x in cur:
        age_id = x[0] #Age group id
        name = x[1] #Age group (children, adult, etc.)
        costume_mapping[name] = age_id
    conn.commit()

    try:
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
    except:
        print("Error inserting CSV data")

    print("Inserting csv data")

    with open('costumes.csv', 'r', encoding = "latin-1") as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        # next(csvReader, None)

        for row in csvReader:
            if len(row) < 1:
                continue
            age_group = ""
            insertion = (None, row[0], costume_mapping[row[1]])
            statement_csv = 'INSERT INTO "Costumes" '
            statement_csv += 'VALUES (?, ?, ?) '
            cur.execute(statement_csv, insertion)
            conn.commit()
        conn.close()

init_db()
insert_json_data()
insert_age_group_data()
insert_csv_data()


#Questions for Matt:
#2. How to properly use Class for scraping?
#3. what to use as primary/foreign key for database?
    #3 tables: halloween costumes, movies, age_group
    #reference age_group ID in halloween costume table
    #age group table - hard code (make by self)


#Plotly Bar Charts
#Plan:
    #Graph 1: 4 bars- 1 is the amount of superhero movies in list, 2 is number
    #of superhero costumes in children costumes, 3 is for adults 18-34,
    #4 is for adults 35+
    #y-axis is percentage (percent of movies that are superhero, percent of )

import plotly.plotly as py
import plotly.graph_objs as go

def movies_average_ratings_graph():
    movie_votes = []
    movie_titles = []

    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    query = "SELECT VoteAverage, Title FROM Movies ORDER BY VoteAverage DESC LIMIT 10 "
    cur.execute(query)

    for x in cur:
        movie_votes.append(x[0])
        movie_titles.append(x[1])

    trace0 = go.Bar(
    x=movie_titles,
    y=movie_votes,
    marker=dict(
        color=['rgba(222,45,38,0.8)', 'rgba(222,45,38,0.8)',
               'rgba(222,45,38,0.8)', 'rgba(222,45,38,0.8)',
               'rgba(222,45,38,0.8)', 'rgba(222,45,38,0.8)',
               'rgba(222,45,38,0.8)', 'rgba(222,45,38,0.8)',
               'rgba(222,45,38,0.8)', 'rgba(222,45,38,0.8)',]),
    )

    data = [trace0]
    layout = go.Layout(
        title='Top 10 Highest Rated Movies for 2016 (By Average Rating)',
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='color-bar')

def movies_most_popular_graph():
    movie_popularity = []
    movie_titles = []

    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    #query = "SELECT Popularity, Title FROM Movies LIMIT 10 "
    query = "SELECT Popularity, Title FROM Movies ORDER BY Popularity DESC LIMIT 10 "

    cur.execute(query)

    for x in cur:
        movie_popularity.append(x[0])
        movie_titles.append(x[1])

    trace0 = go.Bar(
    x=movie_titles,
    y=movie_popularity,
    marker=dict(
        color=['rgb(8,48,107)', 'rgb(8,48,107)', 'rgb(8,48,107)', 'rgb(8,48,107)',
        'rgb(8,48,107)', 'rgb(8,48,107)', 'rgb(8,48,107)', 'rgb(8,48,107)', 'rgb(8,48,107)', 'rgb(8,48,107)',]),
    )

    data = [trace0]
    layout = go.Layout(
        title='Top 10 Most Popular Movies of 2016',
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='color-bar')

def movies_vote_count_graph():
    movie_votes = []
    movie_titles = []

    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    query = "SELECT VoteCount, Title FROM Movies ORDER BY VoteCount DESC LIMIT 10 "
    #query = "SELECT VoteAverage, Title FROM Movies ORDER BY VoteAverage DESC LIMIT 10 "
    cur.execute(query)

    for x in cur:
        movie_votes.append(x[0])
        movie_titles.append(x[1])

    trace0 = go.Bar(
    x=movie_titles,
    y=movie_votes,
    marker=dict(
        color=['rgba(50,171,96,0.7)', 'rgba(50,171,96,0.7)',
               'rgba(50,171,96,0.7)', 'rgba(50,171,96,0.7)',
               'rgba(50,171,96,0.7)', 'rgba(50,171,96,0.7)',
               'rgba(50,171,96,0.7)', 'rgba(50,171,96,0.7)',
               'rgba(50,171,96,0.7)', 'rgba(50,171,96,0.7)',]),
    )

    data = [trace0]
    layout = go.Layout(
        title='Top 10 Movies of 2016 By Vote Count',
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='color-bar')

# def animal_graph():
#     pass
#
# def political_graph():
#     pass

#movies_average_ratings_graph()
#movies_most_popular_graph()
#movies_vote_count_graph()


#Interactive Command Line:
print("----------------------------------------------------------")
print("-------------- Welcome to my final project! --------------")
print("----------------------------------------------------------")

user_input = input("Please enter a command or 'help' for more options: ")
while user_input != 'exit':
    #First data visualization:
    if user_input == "graph top 10 movies ratings":
        movies_average_ratings_graph()
#         print graph superhero
#         print graph princess
#         print graph animal
#         print graph political
    #Second data visualization:
    elif user_input == "graph top 10 movies popularity":
        movies_most_popular_graph()
    #Third data visualization:
    elif user_input == "graph top 10 movies vote count":
        movies_vote_count_graph()
    #Fourth Data Visualization:
    elif 'movies' in user_input[0:6]:
        result_number = str(user_input[7])
        movies_list = []
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
        query = "SELECT Title FROM Movies ORDER BY Popularity DESC "
        cur.execute(query)

        for x in cur:
            movies_list.append(x[0])

        movies_list = movies_list[result_number]

        for x in range(len(movies_list)):
            print(str(x + 1) + ". " + movies_list[x].__str__())

        print("\n")

        #print top however many movies the user wants

    elif user_input == "costumes children":
        childrens_costumes = []

        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
        query = "SELECT CostumeName FROM Costumes WHERE AgeGroupId = 1 "
        cur.execute(query)

        for x in cur:
            childrens_costumes.append(x[0])

        for x in range(len(childrens_costumes)):
            print(str(x + 1) + ". " + childrens_costumes[x].__str__())

        print("\n")

    elif user_input == "costumes adults 18-34":
        adults_18_34_costumes = []

        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
        query = "SELECT CostumeName FROM Costumes WHERE AgeGroupId = 2 "
        cur.execute(query)

        for x in cur:
            adults_18_34_costumes.append(x[0])

        for x in range(len(adults_18_34_costumes)):
            print(str(x + 1) + ". " + adults_18_34_costumes[x].__str__())

        print("\n")

    elif user_input == "costumes adults 35+":
        adults_35_costumes = []

        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
        query = "SELECT CostumeName FROM Costumes WHERE AgeGroupId = 3 "
        cur.execute(query)

        for x in cur:
            adults_35_costumes.append(x[0])

        for x in range(len(adults_35_costumes)):
            print(str(x + 1) + ". " + adults_35_costumes[x].__str__())

        print("\n")

    elif user_input == "costumes pets":
        pets_costumes = []

        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
        query = "SELECT CostumeName FROM Costumes WHERE AgeGroupId = 4 "
        cur.execute(query)

        for x in cur:
            pets_costumes.append(x[0])

        for x in range(len(pets_costumes)):
            print(str(x + 1) + ". " + pets_costumes[x].__str__())

        print("\n")

    elif 'help' in user_input[0:4]:
        #print("Enter 'graph' and 'superhero', 'princess', 'animal', or 'political' to see the graph for respective movies and costumes. ")
        print("Enter 'movie' and a number to see the most popular movies for 2016. ")
        print("Enter 'costume' and a group name to see the top ten costumes for that group. ")
        print("Enter 'exit' to end the program. ")
        break
        #print a list of possible commands + explanations
    elif user_input == "exit":
        print("Bye!")
        break
    else:
        print("I'm sorry, I don't understand. Please enter a valid command. ")

    user_input = input("Please enter a command or 'help' for more options: ")
