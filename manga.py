import uuid

class Manga:
    def __init__(self, title="", manga_id=0, description="Description",
                 status="N/A", tags=[], chapters=[], following=False):
        self.title       = title
        self.manga_id    = manga_id
        self.description = description
        self.status      = status
        self.tags        = tags
        self.chapters    = chapters
        self.following   = following

    def __str__(self):
        return f"\"{self.title}\", {len(self.chapters)} chapters"

class Chapter:
    def __init__(self, chapter_id=uuid.uuid4(), data=[],
                 chapter_hash="", title="", chapter=-1,
                 language="Toki Pona", read=False):
        self.chapter_id   = chapter_id
        self.data         = data
        self.chapter_hash = chapter_hash
        self.title        = title
        self.chapter      = chapter
        self.read         = read

    def __str__(self):
        return f"Chapter {self.chapter}: \"{self.title}\""
