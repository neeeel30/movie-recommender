import pickle
import streamlit as st
import requests

# Function to load data
def load_data(movies_file_path, similarity_file_path, descriptions_file_path):
    with open(movies_file_path, "rb") as movies_file, \
         open(similarity_file_path, "rb") as similarity_file, \
         open(descriptions_file_path, "rb") as descriptions_file:
        movies_data = pickle.load(movies_file)
        similarity_data = pickle.load(similarity_file)
        descriptions_data = pickle.load(descriptions_file)
    return movies_data, similarity_data, descriptions_data

def join_overview(overview):
    return ' '.join(overview)

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"  # Replace YOUR_API_KEY with your API key
    try:
        data = requests.get(url).json()
        poster_path = data['poster_path']
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return None
    except requests.RequestException as e:
        st.error("Error fetching movie poster. Please try again later.")
        st.stop()

# Function to recommend movies
def recommend_movies(selected_movie, movies, similarity, descriptions):
    try:
        index = movies[movies['title'] == selected_movie].index[0]
    except IndexError:
        st.error("Selected movie not found in the dataset. Please choose another movie.")
        st.stop()
    
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_descriptions = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movie_posters.append(poster_url)
            recommended_movie_names.append(movies.iloc[i[0]].title)
            recommended_movie_descriptions.append(join_overview(descriptions[descriptions['movie_id'] == movie_id]['overview'].values[0]))
    return recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions
# Main function
def main():
    # Load data
    movies, similarity, descriptions = load_data(r"D:\PDPU\Coding\Anaconda_Data_Science\Projects\movie Project-main\movies.pkl", r"D:\PDPU\Coding\Anaconda_Data_Science\Projects\movie Project-main\similarity.pkl", r"D:\PDPU\Coding\Anaconda_Data_Science\Projects\movie Project-main\movies_des.pkl")  # Update file paths accordingly

    # Set page configuration
    st.set_page_config(
        page_title="Movie Recommender",
        page_icon="🎬",
        layout="wide"
    )

    # Title
    st.title('Movie Recommender System')

    # Sidebar - User Input
    st.sidebar.header('User Input')
    selected_movie = st.sidebar.selectbox("Select a Movie", movies['title'].values)

    if st.sidebar.button('Get Recommendations'):
        with st.spinner('Fetching Recommendations...'):
            # Get movie recommendations
            recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions = recommend_movies(selected_movie, movies, similarity, descriptions)

            # Display recommendations
            num_recommendations = len(recommended_movie_names)
            if num_recommendations == 0:
                st.warning("No recommendations found for the selected movie.")
            else:
                st.subheader("Recommended Movies")
                for movie_name, poster_url, description in zip(recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions):
                    col1, col2 = st.columns([1, 5])
                    with col1:
                        st.image(poster_url, use_column_width=True)
                    with col2:
                        st.write(f"**{movie_name}**")
                        st.write(description)

if __name__ == "__main__":
    main()


# import pickle
# import streamlit as st
# import requests

# # Function to load data
# def load_data(movies_file_path, similarity_file_path, descriptions_file_path):
#     with open(movies_file_path, "rb") as movies_file, \
#          open(similarity_file_path, "rb") as similarity_file, \
#          open(descriptions_file_path, "rb") as descriptions_file:
#         movies_data = pickle.load(movies_file)
#         similarity_data = pickle.load(similarity_file)
#         descriptions_data = pickle.load(descriptions_file)
#     return movies_data, similarity_data, descriptions_data

# # Function to fetch movie poster
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"  # Replace YOUR_API_KEY with your API key
#     try:
#         data = requests.get(url).json()
#         poster_path = data['poster_path']
#         if poster_path:
#             return f"https://image.tmdb.org/t/p/w500/{poster_path}"
#         else:
#             return None
#     except requests.RequestException as e:
#         st.error("Error fetching movie poster. Please try again later.")
#         st.stop()

# # Function to join the overview strings
# def join_overview(overview):
#     return ' '.join(overview)

# # Function to recommend movies
# def recommend_movies(selected_movie, movies, similarity, descriptions):
#     try:
#         index = movies[movies['title'] == selected_movie].index[0]
#     except IndexError:
#         st.error("Selected movie not found in the dataset. Please choose another movie.")
#         st.stop()
    
#     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#     recommended_movie_names = []
#     recommended_movie_posters = []
#     recommended_movie_descriptions = []
#     for i in distances[1:6]:
#         movie_id = movies.iloc[i[0]].movie_id
#         poster_url = fetch_poster(movie_id)
#         if poster_url:
#             recommended_movie_posters.append(poster_url)
#             recommended_movie_names.append(movies.iloc[i[0]].title)
#             recommended_movie_descriptions.append(join_overview(descriptions[descriptions['movie_id'] == movie_id]['overview'].values[0]))
#     return recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions

# # Main function
# def main():
#     # Load data
#     movies, similarity, descriptions = load_data(r"D:\PDPU\Coding\Anaconda_Data_Science\Projects\movie Project-main\movies.pkl", r"D:\PDPU\Coding\Anaconda_Data_Science\Projects\movie Project-main\similarity.pkl", r"D:\PDPU\Coding\Anaconda_Data_Science\Projects\movie Project-main\movies_des.pkl")  # Update file paths accordingly
#     # Set page configuration
#     st.set_page_config(
#         page_title="Movie Recommender",
#         page_icon="🎬",
#         layout="wide"
#     )

#     # Title
#     st.title('Movie Recommender System')

#     # Sidebar - User Input
#     st.sidebar.header('User Input')
#     selected_movie = st.sidebar.selectbox("Select a Movie", movies['title'].values)

#     if st.sidebar.button('Get Recommendations'):
#         with st.spinner('Fetching Recommendations...'):
#             # Get movie recommendations
#             recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions = recommend_movies(selected_movie, movies, similarity, descriptions)

#             # Display recommendations
#             num_recommendations = len(recommended_movie_names)
#             if num_recommendations == 0:
#                 st.warning("No recommendations found for the selected movie.")
#             else:
#                 st.subheader("Recommended Movies")
#                 for movie_name, poster_url, description in zip(recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions):
#                     col1, col2 = st.columns([1, 5])
#                     with col1:
#                         poster_img = st.image(poster_url, use_column_width=True)
#                         # Add click event handler to toggle full-screen display
#                         poster_img = st.image(poster_url, use_column_width=True)
#                         poster_img._update_content_with_click_handler(poster_url)
#                     with col2:
#                         st.write(f"**{movie_name}**")
#                         st.write(description)

# if __name__ == "__main__":
#     main()

