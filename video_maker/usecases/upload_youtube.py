import httplib2
import os
import random
import time

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

from video_maker.entities.match_data import MatchData


class UploadYoutube:
    def __init__(self, match_data: MatchData) -> None:
        self.__file = r"C:\Users\ilha\Videos\2022-07-06 15-33-02.mp4"
        self.__title = (
            f"{match_data['mvp']['champion']} vs {match_data['loser']} - {match_data['region']} {match_data['mvp']['rank']} Patch {match_data['patch']}")
        self.__description = f"""
    #{match_data['mvp']['champion']} played by {match_data['mvp']['name']} at #{match_data['region']}{match_data['mvp']['rank']}

    Data provided by https://leagueofgraphs.com
    """
        self.__category = "20"
        self.__keywords = [f"{match_data['mvp']['champion']}", "challenger",
                           "leagueoflegends", "replay", "high kda",
                           f"{match_data['region']}"]
        httplib2.RETRIES = 1
        self.__MAX_RETRIES = 10
        self.__RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error)
        self.__RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
        self.__CLIENT_SECRETS_FILE = "./credentials/client_secrets.json"
        self.__YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
        self.__YOUTUBE_API_SERVICE_NAME = "youtube"
        self.__YOUTUBE_API_VERSION = "v3"
        self.__VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")
        self.__MISSING_CLIENT_SECRETS_MESSAGE = f"""
        WARNING: Please configure OAuth 2.0

        To make this sample run you will need to populate the client_secrets.json file
        found at:

          {os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          self.__CLIENT_SECRETS_FILE))}

        with information from the API Console
        https://console.developers.google.com/

        For more information about the client_secrets.json file format, please visit:
        https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        """

    def upload_video(self):
        try:
            self.__initialize_upload()
        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")

    def __build_video_data(self):
        return {
            "file": self.__file,
            "title": self.__title,
            "description": self.__description,
            "category": self.__category,
            "keywords": self.__keywords,
            "privacyStatus": self.__VALID_PRIVACY_STATUSES[1]
        }

    def __get_authenticated_service(self):
        flow = flow_from_clientsecrets(self.__CLIENT_SECRETS_FILE,
                                       scope=self.__YOUTUBE_UPLOAD_SCOPE,
                                       message=self.__MISSING_CLIENT_SECRETS_MESSAGE)

        storage = Storage("./credentials/storage-oauth2.json")
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage)

        return build(self.__YOUTUBE_API_SERVICE_NAME, self.__YOUTUBE_API_VERSION,
                     http=credentials.authorize(httplib2.Http()))

    def __initialize_upload(self):
        youtube = self.__get_authenticated_service()
        options = self.__build_video_data()
        tags = None
        if options['keywords']:
            tags = options['keywords']

        body = dict(
            snippet=dict(
                title=options['title'],
                description=options['description'],
                tags=tags,
                categoryId=options['category']
            ),
            status=dict(
                privacyStatus=options['privacyStatus']
            )
        )

        # Call the API's videos.insert method to create and upload the video.
        insert_request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=MediaFileUpload(
                options['file'], chunksize=-1, resumable=True)
        )

        self.__resumable_upload(insert_request)

    def __resumable_upload(self, insert_request):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print("Uploading file...")
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print(
                            f"Video id {response['id']} was successfully uploaded.")
                        return response['id']
                    else:
                        exit(
                            f"The upload failed with an unexpected response: {response}")
            except HttpError as e:
                if e.resp.status in self.__RETRIABLE_STATUS_CODES:
                    error = f"A retriable HTTP error {e.resp.status} occurred:\n{e.content}"
                else:
                    raise
            except self.__RETRIABLE_EXCEPTIONS as e:
                error = f"A retriable error occurred: {e}"

            if error is not None:
                print(error)
                retry += 1
                if retry > self.__MAX_RETRIES:
                    exit("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print(f"Sleeping {sleep_seconds} seconds and then retrying...")
                time.sleep(sleep_seconds)
