from typing import List, Tuple
from db.sqlite import init_db,insert
from runtime import ImageTAG,HyperlinkTAG,get_task,put_task
from networks import HTTP
from bs4 import BeautifulSoup
from conf import BASEURL
from uuid import uuid4
from loguru import logger
from time import sleep


SLEEP_TIME = 0.5
DISABLE_PARENT_URL = True
DOWNLOAD_FOLDER = "img"
HEXFOLDER="hex"


def load_HTML():
    html = HTTP.get("/")
    return html.text
def download_img(img_obj:ImageTAG):
    """
    download image from url and save to disk
    """
    hexname = uuid4().hex
    url = img_obj.absolute_path
    status = 200
    try:
        resp = HTTP.get(url)
    except Exception as e:
        logger.error(f"download_img: {e}")
        return
    if resp is None:
        return
    with open(f"{DOWNLOAD_FOLDER}/{HEXFOLDER}/{hexname}", "wb+") as f:
        f.write(resp.content)

    with open(f"{DOWNLOAD_FOLDER}/{hexname}.{url.split('.')[-1]}", "wb+") as f:
        f.write(resp.content)
    insert(url, status, hexname, f"{DOWNLOAD_FOLDER}/{HEXFOLDER}/{hexname}")
def process_HTML(parent_url:str,html:str)->Tuple[list[ImageTAG], list[HyperlinkTAG]]:
    """
    returns images, linkes
    tuple(list[ImageTAG], list[HyperlinkTAG])
    list[<img src="...">]
    list[<a href="...">]
    """
    logger.debug(f"parent_url: {parent_url}")
    if DISABLE_PARENT_URL:
        parent_url = ""

    bs = BeautifulSoup(html, "lxml")
    image_list = bs.find_all("img")
    href_list = bs.find_all("a")
    img_obj_list = []
    href_obj_list = []

    for img in image_list:
        img_obj = ImageTAG(img_rel_path=img.get("src"), 
                 img_abs_path=parent_url + img.get("src",""),
                 tag_string=str(img)
                 )
        logger.debug(f"img_obj: {img_obj.absolute_path}")
        img_obj_list.append(img_obj)
        
    for href in href_list:
        if href.get("href") and "http" not in href.get("href"):
            if href.get("href").startswith("#"):
                continue
            href_obj = HyperlinkTAG(url=parent_url + href.get("href"), 
                                          tag_string=str(href))
            logger.debug(f"href_obj: {href_obj.url}")
            href_obj_list.append(href_obj)
    return img_obj_list, href_obj_list

def task_enqueue(task_list:list[ImageTAG]):
    """
    enqueue task to queue
    """
    for task in task_list:
        put_task(task)

def recurse_current_layer(images_tags:List[ImageTAG]):
    for img in images_tags:
        sleep(SLEEP_TIME)
        download_img(img)

        
if __name__ == "__main__":
    init_db()
    img_tags,herf_tags = process_HTML(BASEURL, load_HTML())
    recurse_current_layer(img_tags)
    ...
