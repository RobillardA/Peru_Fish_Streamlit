import streamlit as st
from fastai.vision.all import *
import altair as alt
import pandas as pd
import os
import urllib
import pathlib
from PIL import ImageOps
import pathlib

def main():
    st.title('Peru Fish Classifier')

    for filename in EXTERNAL_DEPENDENCIES.keys():
        download_file(filename)
    
    model = load_model()
    
    st.markdown("Fish photo for classification.")
    image = st.file_uploader("", IMAGE_TYPES)
    if image:
        image_data = image.read()
        st.image(image_data, use_column_width=True)

        prediction = model.predict(image_data)
        
        pred_chart = predictions_to_chart(prediction, classes = model.dls.vocab)
        st.altair_chart(pred_chart, use_container_width=True)

def predictions_to_chart(prediction, classes):
    pred_rows = []
    for i, conf in enumerate(list(prediction[2])):
        pred_row = {'class': classes[i],
                    'probability': round(float(conf) * 100,2)}
        pred_rows.append(pred_row)
    pred_df = pd.DataFrame(pred_rows)
    pred_df.head()
    top_probs = pred_df.sort_values('probability', ascending=False).head(4)
    chart = (
        alt.Chart(top_probs)
        .mark_bar()
        .encode(
            x=alt.X("probability:Q", scale=alt.Scale(domain=(0, 100))),
            y=alt.Y("class:N",
                    sort=alt.EncodingSortField(field="probability", order="descending"))
        )
    )
    return chart    

plt = platform.system()
print(plt)
if plt == 'Linux' or plt == 'Darwin': pathlib.WindowsPath = pathlib.PosixPath
    
@st.cache(allow_output_mutation=True)
def load_model():
    plt = platform.system()

    if plt == 'Linux' or plt == 'Darwin': pathlib.WindowsPath = pathlib.PosixPath
    inf_model = load_learner('perumixed3.pkl', cpu=True)

    return inf_model


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
    "perumixed3.pkl": {
        "url": "https://www.dropbox.com/s/31e6wuwrlm66sco/perumixed3.pkl?dl=1",
        "size": 179319095
    }
}

if __name__ == "__main__":
    main()
