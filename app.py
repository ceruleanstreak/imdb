import streamlit as st 
import pandas as pd

st.title("IMDB Movies and TV Series rankings")

@st.cache(persist=True, allow_output_mutation=True, suppress_st_warning=True)
def load_imdb_data():
    basic = pd.read_table('https://datasets.imdbws.com/title.basics.tsv.gz')
    rating = pd.read_table('https://datasets.imdbws.com/title.ratings.tsv.gz')
    y = basic["startYear"]
    y = pd.to_numeric(y, errors='coerce')
    basic["startYear"] = y
    r = rating["averageRating"]
    r = pd.to_numeric(r, errors='coerce')
    rating["averageRating"] = r
    imdb_wide = pd.merge(basic, rating, left_on = "tconst", right_on = "tconst", how = "left")
    imdb_unsorted = imdb_wide[["primaryTitle", "startYear", "averageRating", "numVotes", "titleType"]]
    imdb = imdb_unsorted.sort_values(by=["averageRating"], axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')
    return imdb

imdb = load_imdb_data()


startYear = st.sidebar.number_input(label = 'Year', min_value=2000, max_value=2020, value=2018, step=1, format=None, key=None)
numVotes = st.sidebar.number_input(label = 'Min num of votes', min_value=0, max_value=1000000, value=30000, step=10000, format=None, key=None)
minRating = st.sidebar.number_input(label = 'Min rating', min_value=1.0, max_value=9.9, value=7.5, step=0.1, format=None, key=None)

x = imdb[(imdb.startYear >= startYear) & (imdb.numVotes >= numVotes) & (imdb.averageRating >= minRating) & (imdb.titleType == "movie")]
st.subheader("Movies")
st.dataframe(x)

y = imdb[(imdb.startYear >= startYear) & (imdb.numVotes >= numVotes) & (imdb.averageRating >= minRating) & ((imdb.titleType == "tvMiniSeries") | (imdb.titleType == "tvSeries"))]
st.subheader("TV Series and Mini Series")
y