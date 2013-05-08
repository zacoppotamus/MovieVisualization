MovieVisualization
==================

#Description

Quick and dirty analysis of the number of films shot in every state. Written in [Processing](http://processing.org) and Python.

##Analysis

This was a very quick hack/proof-of-concept (done for an open-ended assignment in 2 days) and is in no way complete yet. 

I explored many different possibilities with the Python parser regarding the direction of this project. My first thought was
to find a correlation between the budget of certain movies and their user rating. 

Then I decided to account for inflation and
find patterns in the budgets of critically acclaimed movies. 

At the end I settled with the distribution of movies by state*, while showing the movie posters for that states top movies.
You may notice some films appearing twice (eg. The Godfather). That is because their filming locations span different states and have a very high rating.


*The conditions for a movie to be included was for it to have a rating over 6 and at least 12,000 votes.

**You will need to increase the maximum available memory used by Processing through the preferences. 128 MBs seem to work fine.


##Acknowledgments 
The basic functionalities for the Processing sketch are an adaptation of [Ben Fry's](http://benfry.com) example from the book Visualizing Data.

[BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) is friggin' amazing.

An [izac](http://izac.us) joint, 2013.


![Example](https://raw.github.com/zacoppotamus/MovieVisualization/master/Screenshot1.png) 
![Example](https://raw.github.com/zacoppotamus/MovieVisualization/master/ScreenShot2.png)
