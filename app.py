import streamlit as st
import pickle
import pandas as pd
import requests
import time
import bz2
import _pickle as cPickle



def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://drive.google.com/uc?id=1f0EfMNxWi7yoZEGsKEcWn4JZTdo131mc");
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]

    with st.spinner('Wait for it...'):
        time.sleep(2)
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        #fetch poster from Api
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


movie_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movie_dict)

#similarity=pickle.load(open('similarity.pkl','rb'))


similarity = cPickle.load(bz2.BZ2File('similarity.pbz2', 'rb'))
from streamlit_option_menu import option_menu

with st.sidebar:
    selected=option_menu(
        menu_title=None,
        options=["Home","about","Contact"],
        icons=["house","book","envelope"],
        menu_icon="cast",
        default_index=0,

        styles={
            "container":{"padding":"0!important"},
            "icon":{"color":"orange","font-size":"25px"},
            "nav-link":{
                "font-size":"25px",
                "text-align":"left",
                "margin":"0px",
                "--hover-color":"#eee",
            },
            "nav-link-selected":{"background-color":"green"},
        },
    )

if selected=="Home":
    st.markdown("<h1 style='text-align: center;color: skyblue;font-size:110px;'>Cinema Guide</h1>", unsafe_allow_html=True)
    page_bg_img = """
    <style>
    .header {
        margin-bottom: 50em;
        color: #CCCCFF;
        # color: #6495ED;
        font-weight: bold;
        font-size: 25px;
        text-align: center;
        margin-bottom: -15em;
    }

    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.markdown('<p class="header">Find your perfect film! </p>', unsafe_allow_html=True)
    selected_movie_name = st.selectbox('', movies['title'].values)

    button_style = '''
        <style>
        .stButton button {
            background-color: #87ceeb;
            color: #F5F5DC;
            text-align: center;
            display: block;
            margin: 0 auto;
            padding: 10px 25px;
            border-radius: 5px;
            cursor: default;
            font-weight: bold;
            font-style: italic;
        }
        </style>
    '''

    st.markdown(button_style, unsafe_allow_html=True)

    if st.button('Discover Movies'):

        if st.markdown(
                """
                <style>

                .movie-container {
                    display: flex;
                    overflow-x: auto;
                    gap: 2em;
                    margin-top: 1em;
                }

                .movie-card {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    text-align: center;
                }

                .movie-title {
                    margin-top: 0.3em;
                    margin-bottom: 2.5em;
                    font-weight: bold;
                }
                </style>

                """,
                unsafe_allow_html=True
        ):
            names, posters = recommend(selected_movie_name)

            st.markdown('<div class="movie-container">', unsafe_allow_html=True)
            for name, poster in zip(names, posters):
                st.markdown(
                    """
                    <div class="movie-card">
                        <img src="{}" width="150">
                        <p class="movie-title">{}</p>
                    </div>
                    """.format(poster, name),
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)

if selected=="about":
    st.title("Movie Recommendation System")
    st.write(" A movie recommendation system, or a movie recommender system, is an ML-based approach to filtering or predicting the user's film preferences based on their past choices and behavior.")

if selected=="Contact":
    st.title("Helpline Details")

    import streamlit as st  # pip install streamlit

    st.header(":mailbox: Get In Touch With Me!")

    contact_form = """
    <form action="https://formsubmit.co/saikiranyadav9326@gmail.com" method="POST">
         <input type="hidden" name="_captcha" value="false">
         <input type="text" name="name" placeholder="Your name" required>
         <input type="email" name="email" placeholder="Your email" required>
         <textarea name="Suggestion" placeholder="Your suggestion here"></textarea>
         <button type="submit">Send</button>
    </form>
    """

    st.markdown(contact_form, unsafe_allow_html=True)


    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    local_css("style/style.css")




