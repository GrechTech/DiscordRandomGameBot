from google_images_search import GoogleImagesSearch
import os

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
cx_path = os.path.join(dir_path, "Config", "search_cx.txt")
api_path = os.path.join(dir_path, "Config", "search_api.txt")

cx = ""
api_key = ""

if not os.path.exists(cx_path):
    with open(cx_path, "w+") as f:
        f.write('')
with open(cx_path, "r") as f:
    cx = f.readline().rstrip()

if not os.path.exists(api_path):
    with open(api_path, "w+") as f:
        f.write('')
with open(api_path, "r") as f:
    api_key = f.readline().rstrip()


def do_search(query):
    try:
        gis = GoogleImagesSearch(api_key, cx)

        _search_params = {
            'q': query,
            'num': 1,
            'fileType': 'jpg|gif|png',
        }
        print("Searching")
        gis.search(search_params=_search_params)
        for image in gis.results():
            print(image.url)
            return image.url  # image direct url
        return "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg?20200913095930"
    except Exception as e:
        print(e)
        return "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg?20200913095930"
