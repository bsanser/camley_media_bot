import media
import urllib
import json
import requests
import yaml
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, "config.yaml")
config = yaml.safe_load(open(CONFIG_PATH, encoding="utf8"))

mandatory_fields = ["tvdbId", "tvRageId", "title", "titleSlug", "images", "seasons"]

class SonarrRetriever(media.MediaRetriever):
    def searchForMedia(self, search_term: str):
        results = {}
        query_parameters = urllib.parse.urlencode({'apikey':config['sonarr']['apikey'],'term':search_term })
        media_search_request = requests.get('http://192.168.50.220:8989/api/series/lookup?{query_parameters}'.format(query_parameters=query_parameters) )
        mediaResults = json.loads(media_search_request.text)
        for mR in mediaResults:
            result = media.result(
                mR.get("title"),
                mR.get("year"),
                mR.get("remotePoster"),
                mR.get("overview",''),
                mR.get("tvdbId"),
                "Sonarr")
            results['s'+str(result.id)] = result
        return results
    def addMedia(self, tvdbid: int):
        print("Adding tv show: "+str(tvdbid))
        media_addition_post_data = json.dumps(SonarrRetriever.buildRequest(self, tvdbid))
        addition_request = requests.post('http://192.168.50.220:8989/api/series?apikey={apikey}'.format(apikey=config['sonarr']['apikey']),data=media_addition_post_data )
        if addition_request.status_code == 201:
            return True
        else:
            return False
    def buildRequest(self, tvdbid: int):
        tv_show_request = requests.get('http://192.168.50.220:8989/api/series/lookup?apikey={apikey}&term=tvdb:{tvdbId}'.format(tvdbId=tvdbid, apikey=config['sonarr']['apikey']) )
        tv_show_json = json.loads(tv_show_request.text)
        request_body = {
            "qualityProfileId": "1",
            "addOptions": {
                "ignoreEpisodesWithFiles": "true",
                "ignoreEpisodesWithoutFiles": "false",
                "searchForMissingEpisodes": "true",
            },
            "rootFolderPath": SonarrRetriever.getRootFolder(self),
            "seasonFolder": "true",
        }
        for tv_show in tv_show_json:
            for key, value in tv_show.items():
                if key in mandatory_fields:
                    request_body[key] = value
        return request_body
    def getRootFolder(self) -> str:
        return 'D:\\TV\\'