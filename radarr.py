import media
import urllib
import json
import requests
import yaml
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, "config.yaml")
config = yaml.safe_load(open(CONFIG_PATH, encoding="utf8"))

mandatory_fields = ["tmdbId", "year", "title", "titleSlug", "images"]

class RadarrRetriever(media.MediaRetriever):
    def searchForMedia(self, search_term: str):
        results = {}
        query_parameters = urllib.parse.urlencode({'apikey':config['radarr']['apikey'],'term':search_term })
        media_search_request = requests.get('http://192.168.50.220:7878/api/v3/movie/lookup?{query_parameters}'.format(query_parameters=query_parameters) )
        mediaResults = json.loads(media_search_request.text)
        for mR in mediaResults:
            result = media.result(
                mR.get("title"),
                mR.get("year"),
                mR.get("remotePoster"),
                mR.get("overview",''),
                mR.get("imdbId"),
                "Radarr")
            results['r'+str(result.id)] = result
        return results
    def addMedia(self, imdbid: str):
        print("Adding movie: "+imdbid)
        media_addition_post_data = json.dumps(RadarrRetriever.buildRequest(self, imdbid))
        query_parameters = urllib.parse.urlencode({'apikey':config['radarr']['apikey'] })
        addition_request = requests.post('http://192.168.50.220:7878/api/v3/movie?{query_parameters}'.format(query_parameters=query_parameters),data=media_addition_post_data )
        if addition_request.status_code == 201:
            return True
        else:
            return False
    def buildRequest(self, imdbid: str):
        query_parameters = urllib.parse.urlencode({'apikey':config['radarr']['apikey'],'term':'imdbId:'+imdbid })
        movie_request = requests.get('http://192.168.50.220:7878/api/v3/movie/lookup?{query_parameters}'.format(query_parameters=query_parameters ) )
        movie_json = json.loads(movie_request.text)
        request_body = {
                "qualityProfileId": "1",
                "rootFolderPath": RadarrRetriever.getRootFolder(self),
                "addOptions": {"searchForMovie": "true"},
            }

        for movie in movie_json:
            for key, value in movie.items():
                if key in mandatory_fields:
                    request_body[key] = value
        return request_body
    def getRootFolder(self) -> str:
        return 'D:\\Movies\\'