# Feels_Analyst.py
Feels analyst is a hackathon project developed by @bruno207 with some help from @ocelotsloth with some additional input from @dwbond and @nanderson94 at HackVT 2016.

# The Idea
The application:
1.  Gathers the top tracks in a given country
2. Pulls a snippet of the lyrics for those songs
3. Run those lyrics through a Sentiment analysis python library

The idea is to figure out the current mood of the nation based off of what music they are listening to, specifically based of of their lyrics.

# Data Collection
This data is collected via API calls to Last.fm and Musixmatch and utilizes the NTLK libraries for python for their respective steps.

# Technical Info
This is a django application that collects the data, runs some logic, and dumps it into a database which then displays that data back in a pretty webpage.

# Local Setup
Shoot me a email at dhaynes3@gmu.edu if you are interested in technical setup instructions for local development. 
