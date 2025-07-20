import pandas as pd
from warnings import filterwarnings
filterwarnings("ignore")

columns = ["user_id","item_id","rating","timestamp"]

df = pd.read_csv("file.tsv",sep='\t',names=columns)
movies = pd.read_csv("movies.csv")

## Merge two dataframe via item_id
data = pd.merge(df,movies,on="item_id")

## Calculating the average scores of movies
moviesRatings = data.groupby("title")["rating"].mean().sort_values(ascending=False)
print(moviesRatings)

## Calculating how many votes are cast for movies
rateCounts = data.groupby('title')["rating"].count().sort_values(ascending=False)
print(rateCounts)

## Creating a dataframe with movie titles, average ratings, and number of votes
ratings = pd.DataFrame(data.groupby("title")["rating"].mean())
ratings["numOfRatings"] = pd.DataFrame(data.groupby("title")["rating"].count())
print(ratings)

## Correlation between movies
moviemat = data.pivot_table(index="user_id",columns="title",values="rating")

## For example, find movies similar to The Star Wars movie

##User ratings for the Star Wars movie
starWarsUserRatings = moviemat["Star Wars (1977)"]

similarToStarWars = moviemat.corrwith(starWarsUserRatings)

corrStarWars = pd.DataFrame(similarToStarWars,columns=["Correlation"])
corrStarWars.dropna(inplace=True)
corrStarWars = corrStarWars.join(ratings["numOfRatings"])
mostSimilarToStarWars = corrStarWars[corrStarWars["numOfRatings"]>100].sort_values("Correlation",ascending=False)
print(mostSimilarToStarWars.head(10))
