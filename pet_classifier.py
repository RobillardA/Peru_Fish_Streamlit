import streamlit as st
from fastai.vision.all import *
import os
import urllib

def main():
    st.title('Pet Classifier')

    for filename in EXTERNAL_DEPENDENCIES.keys():
        download_file(filename)
    
    image = st.file_uploader("Upload a photo for classification", IMAGE_TYPES)
    if image:
        image_data = image.read()
        st.image(image_data, use_column_width=True)

def download_file(file_path):
    # Don't download the file twice. (If possible, verify the download using the file length.)
    if os.path.exists(file_path):
        if "size" not in EXTERNAL_DEPENDENCIES[file_path]:
            return
        elif os.path.getsize(file_path) == EXTERNAL_DEPENDENCIES[file_path]["size"]:
            return

    # These are handles to two visual elements to animate.
    weights_warning, progress_bar = None, None
    try:
        weights_warning = st.warning("Downloading %s..." % file_path)
        progress_bar = st.progress(0)
        with open(file_path, "wb") as output_file:
            with urllib.request.urlopen(EXTERNAL_DEPENDENCIES[file_path]["url"]) as response:
                length = int(response.info()["Content-Length"])
                counter = 0.0
                MEGABYTES = 2.0 ** 20.0
                while True:
                    data = response.read(8192)
                    if not data:
                        break
                    counter += len(data)
                    output_file.write(data)

                    # We perform animation by overwriting the elements.
                    weights_warning.warning("Downloading %s... (%6.2f/%6.2f MB)" %
                        (file_path, counter / MEGABYTES, length / MEGABYTES))
                    progress_bar.progress(min(counter / length, 1.0))

    # Finally, we remove these visual elements by calling .empty().
    finally:
        if weights_warning is not None:
            weights_warning.empty()
        if progress_bar is not None:
            progress_bar.empty()
    
    return

IMAGE_TYPES = ["png", "jpg"]

EXTERNAL_DEPENDENCIES = {
    "pet_classifier_resnet34.pkl": {
        "url": "https://www.dropbox.com/s/feox6arze2gc14q/pet_classifier_resnet34.pkl?dl=1",
        "size": 87826330
    }
}

if __name__ == "__main__":
    main()