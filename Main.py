import json
import os
from whoosh.fields import Schema, TEXT, ID
from whoosh import index
from whoosh.qparser import QueryParser

with open("crawled.json", "r", encoding="utf-8") as f:
    data = json.load(f)

if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

schema = Schema(
    url=ID(stored=True),
    title=TEXT(stored=True),
    content=TEXT
)

ix = index.create_in("indexdir", schema)

writer = ix.writer()
for url in data:
    writer.add_document(
        url=url,
        title=url,
        content=""
    )
writer.commit()
print(f"Indexed {len(data)} entries ✅")

def search_index(query_str):
    ix = index.open_dir("indexdir")
    qp = QueryParser("content", schema=ix.schema)
    q = qp.parse(query_str)

    with ix.searcher() as searcher:
        results = searcher.search(q, limit=10)
        for hit in results:
            print(f"Title: {hit['title']}, URL: {hit['url']}")

search_index("Python")

