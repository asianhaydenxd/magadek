from manga import *

import requests as req
import json
import os

#Gets a list of manga
#Name, if left blank, will just get the newest manga
#Limit has a cap of 100 manga
def get_manga(title="", limit=10, offset=0):
    #Request the manga list from Mangadex and put it into a dictionary
    r = req.get("https://api.mangadex.org/manga",
                params={"title": title, "limit": limit, "offset": offset, "order[updatedAt]": "desc"})
    d = json.loads(r.text)

    #Create and return instances of the Manga class for each manga
    #with all the data they need(save for chapter list)
    manga_list = []
    for result in d["results"]:
        data = result["data"]
        attr = data["attributes"]
        manga = Manga(
            title      =attr["title"]["en"],
            manga_id   =data["id"],
            description=attr["description"],
            status     =attr["status"],
            tags       =attr["tags"])
        manga_list.append(manga)
    return manga_list

#Gets a list of the chapters for a specific manga
#Honestly just set limit to 100 in almost all cases
def get_chapters(manga, limit):
    #Multiplier for the offset for getting ALL chapters
    count = 0
    chapters = []
    #Until there are no more chapters to get:
    while True:
        #Request chapters from manga
        r = req.get("https://api.mangadex.org/chapter",
                params={"manga": manga.manga_id, "limit": limit, "offset": limit * count})
        #Attempt to load the givin data into a json
        #If it fails, its likely empty, meaning there are no more chapters
        #So it just breaks the loop
        try:
            d = json.loads(r.text)
        except:
            break
        #If it succeeds to get the chapters
        if(r.status_code == 200):
            #Go through each ENGLISH chapter
            #and load the data for each in its own Chapter instance then return the list
            for result in d["results"]:
                if result["data"]["attributes"]["translatedLanguage"] == "en":
                    data = result["data"]
                    attr = data["attributes"]
                    chapter = Chapter(
                        chapter_id  =data["id"],
                        data        =attr["data"],
                        chapter_hash=attr["hash"],
                        title       =attr["title"],
                        chapter     =attr["chapter"])
                    chapters.append(chapter)
            #Increase the multiplier in the case that there are still chapters to get
            count += 1
    return chapters

#Download a specific chapter at a given path
#END THE PATH IN A / OR IT WILL FUCK EVERYTHING UP
def download_chapter(chapter, dl_path):
    #Request the link to the pages
    r = req.get(f"https://api.mangadex.org/at-home/server/{chapter.chapter_id}")
    link = json.loads(r.text)["baseUrl"]

    #Build the url to the pages
    url = f"{link}/data/{chapter.chapter_hash}/"

    #Make sure the path to each folder exists to place the pages in
    if(os.path.exists(dl_path) == False):
        os.mkdir(dl_path)
    if(chapter.chapter == None):
        dl_path = dl_path + f"/{chapter.title}"
    elif(chapter.title == None):
        dl_path = dl_path + f"/{chapter.chapter}"
    else:
        dl_path = dl_path + f"/{chapter.chapter}_{chapter.title}"
    if(os.path.exists(dl_path) == False):
        os.mkdir(dl_path)

    #Download each page from the url built above and the page data
    for page in chapter.data:
        page_link = url + page
        page_path = f"{dl_path}/{page}"
        #Only download the image if it doesn't already exist
        if(os.path.exists(page_path) == False):
            r = req.get(page_link)
            with open(page_path, "wb") as file:
                file.write(r.content)

#Things to do when this file is ran as the main file
#Really just for testing if things work
if __name__ == "__main__":
    title = input("Manga title: ")

    print("Getting manga...")
    manga_list = get_manga(title=title)

    count = 0
    for manga in manga_list:
        print(f"{count}: {manga.title}")
        count += 1

    manga_num = int(input("Manga number: "))
    manga = manga_list[manga_num]
    manga.chapters = get_chapters(manga, 100)

    yn = input("Download chapters? Y/N  ")

    if(yn == "Y"):
        print("Downloading chapters...")
        for chapter in manga.chapters:
            path = f"{os.getcwd()}/{manga.title}/"
            download_chapter(chapter, path)

        print("Done!")
        input("Press Enter to continue")

