from google_images_search import GoogleImagesSearch
import os

DIR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))
CX_PATH = os.path.join(DIR_PATH,"Config","search_cx.txt")
API_PATH = os.path.join(DIR_PATH,"Config","search_api.txt")

cx = ""
api_key = ""

if not os.path.exists(CX_PATH):
    with open(CX_PATH, "w+") as f: 
        f.write('')
with open(CX_PATH,"r") as f:
    cx = f.readline().rstrip()

if not os.path.exists(CX_PATH):
    with open(API_PATH, "w+") as f: 
        f.write('')
with open(API_PATH,"r") as f:
    api_key = f.readline().rstrip()

gis = GoogleImagesSearch(api_key, cx)

def DoSearch(query):
    # define search params
    # option for commonly used search param are shown below for easy reference.
    # For param marked with '##':
    #   - Multiselect is currently not feasible. Choose ONE option only
    #   - This param can also be omitted from _search_params if you do not wish to define any value
    _search_params = {
    'q': query,
    'num': 1,
    'fileType': 'jpg|gif|png',
    'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived',
    }

    gis.search(search_params=_search_params)

    for image in gis.results():
        return image.url  # image direct url
    return ""

if __name__ == "__main__":
    print(DoSearch("wipeout ps1 boxart"))