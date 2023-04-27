import base64
import io
import json
import requests
from urllib.request import urlopen
import os
from imdb import Cinemagoer #pip install git+https://github.com/cinemagoer/cinemagoer
from tkinter import *
from PIL import Image,ImageTk
from googleapiclient.discovery import build #pip install googleapi

import time  #for spotify error
from requests import post, get #need for spotify

###########UTELLY
def utelly_lookup(show_name, country=""):
        url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup"

        if country == "":
            querystring = {"term":show_name}
        else:
            querystring = {"term":show_name,"country":country}

        headers = {
            "X-RapidAPI-Key": "41e8cc204emsh2832407514d8be0p1c0e3ejsn292d5a5df10a",
            "X-RapidAPI-Host": "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        return response.json()


def utelly_get_info(show_name, country=""):
        info = utelly_lookup(show_name, country="")
        info_clean = {}
        for i in range(len(info['results'])):
            info_clean[info['results'][i]['name']] = {"location": info['results'][i]['locations'][0]['display_name'],
                                                      "link": info['results'][i]['locations'][0]['url'],
                                                      "imdb_id": info['results'][i]['external_ids']['imdb']['id'][2:],
                                                      "imdb_url": info['results'][i]['external_ids']['imdb']['url'],
                                                      "thumbnail_link": info['results'][i]['picture'],
                                                      "description": "",
                                                      "utelly": True}
        

        ##############CINEMAGOERS MAKES SEARCH TAKE TOO LONG, IMPLEMENT AFTER SEARCH SELECTION
        for i in info_clean:
              ia = Cinemagoer()
              movie = ia.get_movie(info_clean[i]["imdb_id"], info=['plot'])
              plot = movie.get('plot')[0]
            #   synopsis = movie.get('synopsis')

              info_clean[i]["plot"] = plot
            #   info_clean[i]["synopsis"] = synopsis

        return info_clean

# utelly_get_info("pokemon")


########YOUTUBE
# import tkinter as tk
# from googleapiclient.discovery import build

api_key = 'AIzaSyDicEVjVA8YtjG-jA7v9Tw4_uVOLwWwR00'
youtube = build('youtube', 'v3', developerKey=api_key)

def yt_lookup(search):
    request = youtube.search().list(
        part='snippet',
        maxResults=10,
        q=search
    )
    response = request.execute()

    vid_titles = {}

    for item in response['items']:
        if item['id']['kind'] == 'youtube#video':
            vid_id = item['id']['videoId']
            vid_title = item['snippet']['title']
            channel_name = item['snippet']['channelTitle']
            descrip = item['snippet']['description']
            tn_link = item['snippet']['thumbnails']['high']['url']
            vid_titles[vid_title] = {
                "location": "Youtube",
                "channel": channel_name,
                "description": descrip,
                "thumbnail_link": tn_link,
                "link": f"https://www.youtube.com/watch?v={vid_id}"
            }

    return vid_titles


#####SPOTIFY
def spotify_get_token():
    client_id = "b9e8a2e3b50844ffb3e562d55594a2dd"
    client_secret = "6ff0279dc1304406ac1480a3614261e7"
    auth_string = client_id +":"+ client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

token = spotify_get_token()


def spotify_lookup(token, track_name, wait_run=3, wait_time=1):
        
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    query = f"?q={track_name}&type=track&limit=10"
    query_url = url + query

    # "from requests import post, get"
    #"import time"
    # to fix the 429 error!!!
    for i in range (wait_run): ##line 122 ^^^ add wait_run=3, wait_time=1
        result = get(query_url, headers=headers)

        if result.status_code == 429:
            print(f"Rate limit exceeded. Wait few seconds before retrying")
            time.sleep(wait_time)
        else:
            break    #429 error
          
    json_result = json.loads(result.content)["tracks"]["items"] 


    if len(json_result)==0:
        print("no song with this name")
        return None
        
    top_tracks = {}
    for i in range(len(json_result)):
        track = json_result[i]
        top_tracks[track["name"]] = { "location": "Spotify", 
                                        "link": track["href"],
                                        "thumbnail_link": track["album"]['images'][0]["url"],
                                        "duration": round(track["duration_ms"]/(1000*60),2),
                                        "description": track["artists"][0]["name"] }

    return top_tracks

# print(spotify_lookup(token, "pokemon"))


##########GOOGLE BOOKS
# Getting books from Google Books API
def get_books(search):
    API_KEY = "AIzaSyBIqhXR3mSaZUE1sYXTelJ2P5gF6TOEv9o"
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={search}&key={API_KEY}").json()
    books = response.get('items', []) #getting list of books
    return books

# display book information function
def gb_get_info(book):
    book_info = {}
    books = get_books(book)
    for book in books:
        book_info[book['volumeInfo'].get('title', '')] = {"location": "Google Books",
                                                          "link": book['selfLink'],
                                                          "thumbnail_link": book['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
                                                          "description": book['volumeInfo'].get('description', ''),
                                                          "page_count": book['volumeInfo'].get('pageCount', ''),
                                                          "average_rating": book['volumeInfo'].get('averageRating', '')}
     #getting the book info

    # Displaying book info
    # print(book_info['book_url'])
    # display.display(display.Image(url=book_info['thumbnail_url']))
    # print(book_info['title'])
    # print(book_info['description'])
    # print(book_info['page_count'])
    # print(book_info['average_rating'])

    return book_info

# generate book information based on user search
def generate_book():
    search_query = input("Select a book. Enter in the title: ")
    books = get_books(search_query)  # Fetching data for books based on the search query
    if len(books) > 0:     # Checking if any books were found for the search
        for book in books:
            display_book_info(book)  # Displaying book information for each book found in the search query
    else:                  #if there are no books, say no books
        print(f"No books found for the search, {search_query}.")

# def gen_book_dict(title):
#     books = get_books(title)
#     if len(books) > 0:     # Checking if any books were found for the search
#         for book in books:
#             display_book_info(book)  # Displaying book information for each book found in the search query
#     else:                  #if there are no books, say no books
#         print(f"No books found for the search, {search_query}.")


# gb_get_info("the witcher")



##########TKINTER GUI
root = Tk()
root.title("Show Search")
root.geometry("750x750")

# Tkinter widgets needed for scrolling.  The only native scrollable container that Tkinter provides is a canvas.
# A Frame is needed inside the Canvas so that widgets can be added to the Frame and the Canvas makes it scrollable.
canvas1 = Canvas(root, width=750, height=750)
frame1 = Frame(canvas1)
scrollbar = Scrollbar(root)

# Updates the scrollable region of the Canvas to encompass all the widgets in the Frame
def updateScrollRegion():
	canvas1.update_idletasks()
	canvas1.config(scrollregion=frame1.grid_bbox())

# Sets up the Canvas, Frame, and scrollbars for scrolling
def createScrollableContainer():
    canvas1.config(yscrollcommand=scrollbar.set, highlightthickness=0)
    scrollbar.config(orient=VERTICAL, command=canvas1.yview)
    scrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
    canvas1.pack(fill=BOTH, side=LEFT, expand=TRUE)
    frame1.pack(fill=BOTH, expand=TRUE)

    canvas1.create_window(0, 0, window=frame1, anchor=NW)


    frame1.columnconfigure(0, weight=1)
    frame1.columnconfigure(1, weight=1)
    frame1.columnconfigure(2, weight=1)

search = StringVar()
print = StringVar()

def search_widgets():
    label_search = Label(frame1, text="Media Search").grid(row=0, column=1, sticky="nsew")
    search_bar = Entry(frame1, textvariable=search).grid(row=1, column=1, sticky="nsew")
    submit_button = Button(frame1, text="search", command=submit_search).grid(row=2, column=1, sticky="nsew")
    
def kill_widgets():
    for widget in frame1.grid_slaves(column=1): 
        widget.grid_forget()
        widget.destroy()

def select_search(result):
    title = results[result]
    lbl_title = Label(frame1, text=f"Title: {result}", wraplength=730, justify=CENTER)
    lbl_location = Label(frame1, text=f"Location: {title['location']}", wraplength=730, justify=CENTER)
    try:
        if title['utelly']==True:
            ia = Cinemagoer()
            movie = ia.get_movie(title["imdb_id"], info=['plot'])
            plot = movie.get('plot')[0]
            title['description'] = plot
            lbl_description = Label(frame1, text=f"Description: {title['description']}", wraplength=730, justify=CENTER)
    except:
        lbl_description = Label(frame1, text=f"Description: {title['description']}", wraplength=730, justify=CENTER)

    if title["thumbnail_link"] == "":
        info_list = [lbl_title, lbl_location, lbl_description]
    else:
        #get the img from theurl
        response = requests.get(title["thumbnail_link"])
        img_data = response.content
        img = Image.open(io.BytesIO(img_data))

        #changing the img size
        w, h = img.size
        if w > 600:
            ratio = 600 / w
            w = 600
            h = int(h * ratio)
        if h > 600:
            ratio = 600 / h
            h = 600
            w = int(w * ratio)
        img = img.resize((w, h))
        #show img on tkinter!!!
        img_tk = ImageTk.PhotoImage(img)
        img_label = Label(frame1, image=img_tk)
        img_label.image = img_tk

        info_list = [lbl_title, lbl_location, lbl_description, img_label]

    kill_widgets()
    search_widgets()

    i_list = []
    for count in range(len(info_list)):
        i_list.append(count)
    for lbl,i in zip(info_list,i_list):
        lbl.grid(row=i+5, column=1, sticky="nsew")
    
    
    

def submit_search():
    global search
    f_search = search
    # token = spotify_get_token()

    kill_widgets()
    search_widgets()

    global results

    results = utelly_get_info(f_search.get())
    results.update(gb_get_info(f_search.get()))
    results.update(spotify_lookup(token, f_search.get()))
    results.update(yt_lookup(f_search.get()))
    i_list = []
    for count in range(len(results.keys())):
        i_list.append(count)

    Label(frame1, text="").grid(row=3, column=1, sticky="NSEW")
    Label(frame1, text="Search results").grid(row=4, column=1, sticky="NSEW")

    global result
    for result,i in zip(results,i_list):
        if results[result]['location'] == "Youtube":
            Button(frame1, text=f"{result} - {results[result]['channel']} ({results[result]['location']})", textvariable=result, command=lambda result=result: select_search(result)).grid(row=i+5, column=1, sticky="nsew") #COMMAND HAS YET TO BE MADE
        else:
            Button(frame1, text=f"{result} ({results[result]['location']})", textvariable=result, command=lambda result=result: select_search(result)).grid(row=i+5, column=1, sticky="nsew") #COMMAND HAS YET TO BE MADE

    updateScrollRegion()
    search.set("")


    

createScrollableContainer()
search_widgets()


root.mainloop()