import warnings
warnings.filterwarnings("ignore")
import pandas as pd

def prepareData():
    global movies, moviemat, ratings
    
    columns = ["user_id","item_id","rating","timestamp"]

    df = pd.read_csv("./files.tsv",sep='\t',names=columns, encoding="utf-8")
    movies = pd.read_csv("./movies.csv")

    data = pd.merge(df,movies,on="item_id")

    moviesRatings = data.groupby("title")["rating"].mean().sort_values(ascending=False)

    rateCounts = data.groupby('title')["rating"].count().sort_values(ascending=False)

    ratings = pd.DataFrame(data.groupby("title")["rating"].mean())

    ratings["numOfRatings"] = pd.DataFrame(data.groupby("title")["rating"].count())

    moviemat = data.pivot_table(index="user_id",columns="title",values="rating")

def movieCheck(m):
    for i,row in movies.iterrows():
        if m.lower() in row["title"].lower():
            return row["title"]


def recommend(movie):
    mov = movieCheck(movie)
    if not mov:
        return None
    movie = moviemat[mov]
    similarMovie = moviemat.corrwith(movie)
    corrMovie = pd.DataFrame(similarMovie,columns=["Correlation"])
    corrMovie.dropna(inplace=True)
    corrMovie = corrMovie.join(ratings["numOfRatings"])
    mostSimilarMovie = corrMovie[corrMovie["numOfRatings"]>100].sort_values("Correlation",ascending=False)
    listOfFilm = []
    count = 0
    for i,row in mostSimilarMovie.iterrows():
        listOfFilm.append(i)
        count += 1
        if count == 10:
            return listOfFilm[1:]


if __name__ == "__main__":
    prepareData()
    movie = input("Enter the name of a favorite movie: ")
    print('\n'.join(recommend(movie) if recommend(movie) else ["Not Found!"]))
