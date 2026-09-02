import httpx, json, sys
NKIRI_API = "https://thenkiri.com/wp-json/wp/v2"
def get_latest():
    with httpx.Client(timeout=15, follow_redirects=True, headers={"User-Agent":"Mozilla/5.0"}) as c:
        r = c.get(f"{NKIRI_API}/posts", params={"per_page":6,"orderby":"date","order":"desc","_fields":"id,title,featured_media,link,date"})
        r.raise_for_status()
        posts = r.json()
        ids = [p["featured_media"] for p in posts if p.get("featured_media")]
        poster_map={}
        if ids:
            r2 = c.get(f"{NKIRI_API}/media", params={"include": ",".join(map(str,ids)), "_fields":"id,source_url"})
            if r2.status_code==200:
                for m in r2.json():
                    poster_map[m["id"]]=m.get("source_url","")
        out=[]
        for p in posts:
            import re
            title=re.sub(r"<[^>]+>","",p["title"]["rendered"])
            out.append({"title":title,"link":p.get("link",""),"poster":poster_map.get(p.get("featured_media"),""),"date":p.get("date","")[:10]})
        return out
if __name__=="__main__":
    print(json.dumps({"latest": get_latest()}, indent=2))
