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
import torch

import streamlit as st

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
image_colorizer = get_image_colorizer(artistic=True)
print(image_colorizer)

if torch.cuda.is_available():
	torch.backends.cudnn.benchmark = True
	os.environ["CUDA_VISIBLE_DEVICES"] = "0"
else:
	del os.environ["CUDA_VISIBLE_DEVICES"]


def process_image(input_path):
    render_factor = 30
    result = image_colorizer.plot_transformed_image(path='test_images/' + input_path, figsize=(20,20), render_factor=int(render_factor), display_render_factor=True, compare=False)
    return result

if __name__ == '__main__':
    
    uploaded_file = st.file_uploader("Choose an image for Improvisation...", type="jpg")
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image.save('test_images/' + str(uploaded_file.name))
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        image_colorizer = get_image_colorizer(artistic=True)
        results = process_image(uploaded_file.name)
        st.image(results)