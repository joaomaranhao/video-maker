# Youtube channel automation

<div style="text-align: center;"><a href="https://github.com/joaomaranhao/video-maker/blob/main/README_pt_br.md">pt-BR</a></div>

#

The idea of ​​this project is to automate the creation of videos, thumbnails and uploading this material to Youtube.

It is a channel of replays of matches of a game called League of Legends.

The entire process is automated. Once the script is started, it manages, through small steps, to programmatically create content.

The channel can be viewed at this link: [League of Legends Replays](https://www.youtube.com/channel/UC-C_dsVX2-G2UYA9IoD5i3Q)

#

![League of Legends Replays](./docs/images/channel.jpg)

#

## Prerequisites

- [Python](https://www.python.org/downloads/) >=3.9 ;
- [Poetry](https://python-poetry.org/docs/) ;
- [Firefox](https://www.mozilla.org/pt-BR/firefox/new/) >=102 ;
- [OBS](https://obsproject.com/pt-br/download) (Open Broadcaster Software) ;
- Google Account ;

## Technologies

- Web scraping with [Selenium](https://selenium-python.readthedocs.io/) ;
- HTML and CSS for thumbnail creation ;
- RPA (Robotic Process Automation) with [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/) ;
- [Youtube API](https://developers.google.com/youtube/v3/quickstart/python) ;
- OAuth 2 ;

## How it works

The project was created with 5 separate modules, each with its own responsibility.

The modules are in the folder `videomaker/usecases`:

- scrap_lol_data (web scrapper)

  Enter the website, select the match, collect all the necessary data and download the replay (game executable)

  ![League of Legends Replays](./docs/images/match.png)

  #

- data

  Responsible for saving and loading the information received by the web scrapper in a json file

  #

- create_thumbnail

  This module creates a custom thumbnail with HTML and CSS using the information obtained by the web scrapper

  ![League of Legends Replays](./docs/images/thumb.png)

  #

- record_video

  Use PyAutoGUI and PyDirectInput to control the game and OBS to record the game

  #

- upload_youtube

  Responsible for filling information such as title, description and keywords, uploading the video and thumbnail
