import os
from time import sleep
from usecases.data import load
from entities.data_scrapper import DataScrapper
from entities.match_data import MatchData


class CreateThumbnail:
    def __init__(self, data_scrapper: DataScrapper, data: MatchData) -> None:
        self.scrapper = data_scrapper
        self.lol_data = data

    def create_thumbnail(self):
        champion = self.lol_data['mvp']['champion'].replace("'", "").capitalize()
        self.__create_html(
            kda=self.lol_data['mvp']['kda'],
            imgUrl=f'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion}_0.jpg',
            mvp=self.lol_data['mvp']['champion'],
            vs=self.lol_data['loser'],
            region=self.lol_data['region'],
            patch=self.lol_data['patch']
        )
        html_path = os.path.abspath('assets/thumbnail.html')
        print(html_path)
        self.scrapper.driver.get('file://' + html_path)
        sleep(2)
        self.scrapper.driver.set_window_size(1280, 720)
        self.scrapper.driver.save_screenshot('./assets/thumb.png')
        self.scrapper.driver.quit()

    def __create_html(self, kda: str, mvp: str, vs: str, region: str, patch: str, imgUrl: str):
        HTML = """
<!DOCTYPE html>
<html>
    <head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;800&display=swap" rel="stylesheet">
    <style>
        * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Nanum Gothic', sans-serif;
        }
        .container {
        background-image: url('""" + imgUrl + """');
        background-size: cover;
        width: 1280px;
        height: 720px;
        display: flex;
        align-items: center;
        }
        .frame {
        width: 500px;
        height: 600px;
        margin-left: 50px;
        background-color: rgba(100, 100, 100, .4);
        filter: drop-shadow(0px 20px 10px rgba(0, 0, 0, 0.3));
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        font-weight: 800;
        }
        .kda {
        margin-top: 2rem;
        color: yellow;
        font-size: 6rem;
        display: flex;
        justify-content: center;
        }
        .match {
        display: flex;
        flex-direction: column;
        align-items: center;
        color: white;
        font-size: 3rem;
        }
        .mvp {
        font-size: 5rem;
        }
        .vs {
        font-size: 2rem;
        }
        .region {
        background-color: aquamarine;
        color: #444;
        padding: .5rem 1.5rem;
        border-radius: 2rem;
        font-size: 2rem;
        }
        .patch {
        color: white;
        font-size: 1.5rem;
        margin-bottom: 2rem;
        }
    </style>
    </head>""" + f"""
<body>
    <div class="container">
    <div class="frame">
        <div class="kda">
        <p>{kda}</p>
        </div>
        <div class="match">
        <p class="mvp">{mvp}</p>
        <p class="vs">vs</p>
        <p>{vs}</p>
        </div>
        <div class="region">
        <p>{region}</p>
        </div>
        <div class="patch">
        <p>Patch {patch}</p>
        </div>
    </div>
    </div>
</body>
</html>
"""
        with open("./assets/thumbnail.html", "w") as f:
            f.write(HTML)
