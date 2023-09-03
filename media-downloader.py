import sonarr

o1=sonarr.SonarrRetriever()

for r in o1.searchForMedia("t2"):
    print(r.title)
    print(r.year)
    print(r.poster)
    print(r.overview)