Welcome to Shannon's Final Project!

My goal for this project was to obtain data for the 100 most popular movies of 2016
and compare that data to the most popular Halloween Costumes for 2016 to see if
there was a correlation between the two.

Data Sources Used:
1. TMDB (The Movie Database) API- I used this API to obtain data on the top 100
most popular movies for 2016, in descending order by popularity. In order to
access movie data from this specific API, you need to sign up on the website for
an API key. To receive an API key, follow this link: https://www.themoviedb.org/documentation/api
and sign up (it's free). Then, access you account by clicking the icon in the top
right corner of the screen and click account settings, then API. That page is where
you will find your API key. This key is needed to make requests to the database
to obtain ANY movie data. To incorporate the key into the program, make a file "secrets.py"
and set a variable equal to the API key. Then, in your main code file, import
secrets.py and utilize that variable to access the API key. This is so the key is
not made public when you push your code to GitHub.

2. Web Scraping: NRF Consumer Trends for Halloween Costumes in 2016
I utilized web scraping to obtain data from this website for the top 10 most popular
Halloween costumes for 2016 for children, adults ages 18-34, adults ages 35 and up,
and pets. To access this data, you need to make a request to the website and use
BeautifulSoup to parse through the html and work with it. When that is done, you need
to use the developer tools on the website to find the correct divs and tags, and
iterate through those to get the data you want. Once that is done, add that information
to a list. From there, you can further manipulate the data to add it to a database
or perform other functions on it.

Run the Program:
Run the program in your terminal/command line. The program will prompt you for a command.
If you are unsure of what command to input, enter "help" for more options and you will see
a list of possible commands and what those commands will return. Graph commands will return
Plotly graphs, which will open a browser window to display the specified graph.

Code Structure:
My code is structured in such a way that first, data is obtained from the TMDB API then
added to a cache file. Next, data is obtained from the website I scraped and that data
is added to a cache file and written to a CSV. Then, I create the database and use the
respective JSON and CSV files to write to the Costume, AgeGroup, and Movie tables. Then,
I use Plotly to create four graphs with data from the database. Finally, I create my
interactive command line to prompt the user for input.

Important processing functions include get_tmdb_data, which I user to obtain data from the
TMDB API, scrape_halloween_costumes, which I use to obtain data from the web page, init_db,
which I user to define the database and tables, then three separate functions write the
web data to each of my three database tables, then four functions are used to make the
Plotly graph for my interactive command line, and these graphs are called depending on the
user's input in the interactive command line.

A HalloweenCostumes class is written for the scraped data (from the Halloween Costumes website).

To create my cache file for the API data and scraped data, I wrote a cache function to
input the data into a cache file, and each file contains a dictionary with the data from the
API and the scraped web page, respectively.

A dictionary is used to map the foreign key onto the Costumes table in my database.

To choose presentation options, enter "help" in the command line to see a list of graph options
and what to input to see those graphs and other visualizations.
