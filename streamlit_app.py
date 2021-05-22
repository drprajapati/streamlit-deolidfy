import uuid

from deoldify.visualize import *
from app_utils import download
from app_utils import generate_random_filename
from app_utils import clean_me
from app_utils import clean_all
from app_utils import create_directory
from app_utils import get_model_bin
from app_utils import convertToJPG
import fastai

import streamlit as st

def process_image(input_path):
    render_factor = 30
    output_path = os.path.join(results_img_directory, os.path.basename(input_path))
    try:
        result = image_colorizer.plot_transformed_image(path='test_images/' + input_path, figsize=(20,20), render_factor=int(render_factor), display_render_factor=True, compare=False)
    except:
        convertToJPG('test_images/' + input_path)
        result = image_colorizer.plot_transformed_image(path='test_images/' + input_path, figsize=(20,20), 
        render_factor=int(render_factor), display_render_factor=True, compare=False)
            
    return result

if __name__ == '__main__':
    global upload_directory
    global results_img_directory
    global image_colorizer
    global ALLOWED_EXTENSIONS
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

    results_img_directory = '/data/result_images/'
    create_directory(results_img_directory)

    model_directory = '/data/models/'
    create_directory(model_directory)
    
    uploaded_file = st.file_uploader("Choose an image for Improvisation...", type="jpg")
    artistic_model_url = "https://data.deepai.org/deoldify/ColorizeArtistic_gen.pth"
    
    get_model_bin(
    artistic_model_url, os.path.join(model_directory, "ColorizeArtistic_gen.pth")
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image.save('test_images/' + str(uploaded_file.name))
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        image_colorizer = get_image_colorizer(artistic=True)
        results = process_image(uploaded_file.name)
        st.image(results)