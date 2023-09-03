import abc

class result:
    def __init__(self, title, year, poster, overview, id, source):
        self.title = title
        self.year = year
        self.poster = poster
        self.overview = overview
        self.id = id
        self.source = source

    def __str__(self):
        return f'Title:{self.title}, Year: {self.year}, Poster: {self.poster}, Overview:{self.overview}, id: {self.id}, source: {self.source}'
    
class MediaRetriever( abc.ABC ) :
    @abc.abstractclassmethod
    def searchForMedia(self, search_term: str ) -> list[result]:
        pass
    @abc.abstractclassmethod
    def addMedia(self, tvidb: int) -> bool:
        pass