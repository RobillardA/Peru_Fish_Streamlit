import streamlit as st
from fastai.vision.all import *
import altair as alt
import pandas as pd
import os
import platform
import pathlib
import gdown
from PIL import ImageOps

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
        
        pred_chart = predictions_to_chart(prediction, classes=model.dls.vocab)
        st.altair_chart(pred_chart, use_container_width=True)

def predictions_to_chart(prediction, classes):
    pred_rows = []
    for i, conf in enumerate(list(prediction[2])):
        pred_row = {'class': classes[i],
                    'probability': round(float(conf) * 100, 2)}
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
if plt == 'Linux' or plt == 'Darwin': 
    pathlib.WindowsPath = pathlib.PosixPath

@st.cache_resource
def load_model():
    plt = platform.system()
    if plt == 'Linux' or plt == 'Darwin': 
        pathlib.WindowsPath = pathlib.PosixPath
    inf_model = load_learner('perumixed3.pkl', cpu=True)
    return inf_model

def download_file(file_path):
    # Check if the file already exists and is the correct size
    if os.path.exists(file_path):
        if "size" in EXTERNAL_DEPENDENCIES[file_path] and os.path.getsize(file_path) == EXTERNAL_DEPENDENCIES[file_path]["size"]:
            return
        else:
            # If the size is incorrect, delete the file and re-download
            os.remove(file_path)

    weights_warning, progress_bar = None, None
    try:
        weights_warning = st.warning(f"Downloading {file_path}...")
        progress_bar = st.progress(0)
        
        # Use gdown to download the file from Google Drive
        gdown.download(EXTERNAL_DEPENDENCIES[file_path]["url"], file_path, quiet=False)
        
    finally:
        if weights_warning is not None:
            weights_warning.empty()
        if progress_bar is not None:
            progress_bar.empty()
    
    # Verify file size after download
    if os.path.getsize(file_path) != EXTERNAL_DEPENDENCIES[file_path]["size"]:
        st.error(f"Failed to download {file_path} correctly. Size mismatch.")
        os.remove(file_path)

    return

IMAGE_TYPES = ["png", "jpg"]

EXTERNAL_DEPENDENCIES = {
    "perumixed3.pkl": {
        "url": "https://drive.google.com/uc?export=download&id=17Dxdvc4OpsFI0QEeQgh7oVspWoNQGuZ1",  # Direct download link from Google Drive
        "size": 179319095  # Ensure the correct file size is provided
    }
}

if __name__ == "__main__":
    main()
