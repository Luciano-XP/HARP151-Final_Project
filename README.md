
## Harp 151 - Final Project
#  Multimedia Search Engine
## Spring, 2023
### [Project Proposal](https://docs.google.com/document/d/1hoyl1yPXKRPsoHOoqWCAK6LXWF1yyHn65geK09LMiUc/edit?usp=sharing#)
### [User Interviews](https://docs.google.com/document/d/1BRhGtoM6INhmK_BLwBfEmgSFrSo63CiDlrNESPc18rE/edit?usp=sharing#)

[GitHub Repository](link_ADDING_LATER#)

[Presentation slides](#https://docs.google.com/presentation/d/14d3NIA_TCjUVDv4uSWpNST-GYOt-kthORkwNdIs9MIE/edit?usp=sharing)

[Demo Video](ADDING_FOR_THE_FINAL#) 

### Team:  
### Luciano Pomara, Samuel Jung, Nagima Dubanaeva & Christopher Sullivan

***

## Project Description 

Our project, "Multimedia Search Engine", uses APIs and Tkinter to provide the user with a program that looks up entertainment content based on specific words. This might seem similar to Google, however, on Google unless you specify which platform you want content from it gives you mostly textual results. You have to use a lot of filtering before you get to something that you actually wanted and were looking for in the first place.
* For example, if you search "spring" this is the type of result you would receive:
![image](image.png)
However, with our program, upon searching up "spring" you will receive content from YouTube, Spotify, Google Books, and Movies involving the word "spring" in it, without filtering beforehand.

***    
      

## Program Design 

* While brainstroming on your project, this is what we kind of envisoned for our project
  ![image](image_2.png)
When we first started on our project, we had a good knowledge of APIs, JSON, and HTML. We were planning on implementing our program into an html. However, we realized that it would be difficult to do and we didn't have confidence or enough experience for that. We decided on using Tkinter.
* This is what our earlier program looked like. It was put together by our Project Manager. The front end is very similar to Google.
  ![image](image_3.png)

* Final version (prototype) of the project:
  ![image](image_9.png)

## Project Structure 
The Project is broken down into the following file structures:

* main.py - GUI & Tkinter Window that combines following APIs together
  * TV movie search API
  * YouTube API
  * Google Books API
  * Spotify API

The code for pulling information from specific API is generally the same which made it easier to combine them together into one GUI
***

## Tasks and Responsibilities 

   * All of the team members have participated in the **coding, debugging, and testing** of the program. Since our program uses four different APIs, each member was assigned an API to work with.

### Project Manager - Lucian Pomara
Focused on organization and making sure the team works effectively during our meetings. Created weekly goals for the team in order to have effective weekly meetings and stay on top of the deadlines. Mainly worked on the GUI and putting all of the APIs into one window.
Worked with the **Movie Search API**, learned the ins and outs of the API.

### Researcher - Samuel Jung 
Was responsible for the **Google Books API**, focused on pulling information from the API. Did so by first creating a parser for the API using functions which was assigned for lab 9. Then modified the structure of the code to fluently be integrated into the group's code. Lastly, made final modifications and placed the Google Books API code into the group's Tkinter format.

### Data Gatherer -  Nagima Dubanaeva 
Worked on the **Spotify API**, focused on pulling necessary information from the API. Worked on debugging any issues regarding the Spotify API. The main task involved learning the structure of the Spotify API and researching how to get the token in order to use the API.

### User Research Lead -  Christopher Sullivan
Worked on the **YouTube API**, focused on pulling necessary information from the API. Fixed any errors regarding the YouTube API, gathered data on what would be effective ways to make the program user-friendly. First made wrappers with wrong functions so had to rewrite code, but integrated it well into entire project.

## Testing

* The code was tested on a case-by-case basis. Whenever a feature did not work as intended, the code would be examined at the line where the error occurred or if there was no error message. Also, we tried to keep the code as dry as possible.
* Since every member focused on a separate API, everyone was responsible for debugging their code before putting it all together into a tkinter window.
    
    * For example, there were some issues with the Spotify API, since the program needed a new token every hour to run. To fix the code, the token was implemented into the program as one of the functions so each time the code is run there is a new token generated. This might not be the most effective solution, however, it worked for our program and has not been an issue so far.
      
* Three members (other than the PM) were responsible for finding users to try the program and comment on any dislikes and likes regarding the program. The feedback was used to make any changes to the prototype.

## ATP

| Step                  | Procedure     | Expected Results  | Image |
| :----------------------:|:-------------:| :-----------------:| :---------: |
|  1  | Running the code |  the Tkinter window opens up to the search bar with a "search" button  | ![image](image_4.png)|
|  2  |The user types a word based on their interest|  Buttons containing results from the four APIs (YT, Spotify, Google Books and movies) are returned based on the word searched up | ![image](image_7.png) |
|  3 |The user makes a selection and clicks on one of the buttons|  the Tkinter opens a new window containing info on their selection  | ![image](image_8.png)|
