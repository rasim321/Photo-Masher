import streamlit as st
import requests
from PIL import Image
from database import return_max_content_id, return_max_style_id
import time
import uvicorn

# uvicorn.run("app.app:app", host="0.0.0.0")
prefix = "https://photo-masher.herokuapp.com"

#Set the title
st.title("Welcome to photo masher.")

#Instructions
st.text("Step 1: Upload images")
st.text("Step 2: Hit Mash!")

#Photo uploader for content
content_image = st.file_uploader("Choose a content image")
if content_image is not None:
    content_file = {"uploaded_file": content_image}
    content_res = requests.post(f"{prefix}/content", files=content_file)

#Photo uploader for style
style_image = st.file_uploader("Choose a style image")
if style_image is not None:
    style_file = {"style_file": style_image}
    style_res = requests.post(f"{prefix}/style", files=style_file)
    

upload = st.button("Show Images")

if upload:
    if content_image is not None:
        st.text("Content Photo:")
        st.image(content_image, width=500)
    else:
        st.text("You haven't uploaded a content photo")
    
    if style_image is not None:
        st.text("Style Photo:")
        st.image(style_image, width=500)
    else:
        st.text("You haven't uploaded a style photo")


#Helper function to get the composite image
def comp_image():

    content_id = return_max_content_id()
    style_id = return_max_style_id()

    get_content = requests.get(f"{prefix}/get_content/{content_id}")
    get_style = requests.get(f"{prefix}/get_style/{style_id}")

    comp_req = requests.get(f"{prefix}/composite?content_id={content_id}&style_id={style_id}")
    comp_image = Image.open('static/composites/comp.JPEG')

    return comp_image

#Mash Button
if st.button("Mash"):
    if content_image and style_image:
        mashed_image = comp_image()
        time.sleep(0.5)
        st.text("Mashed Photo:")
        st.image(mashed_image, width=600)

    
    else:
        st.text("Please upload a content image and a style image")


##Logic for alternative design where there is an uploader button
# upload = st.button("Upload Images")

# flag = False

# displays a button
# if upload:
#     flag = True
#     if content_image is not None:
#         content_file = {"uploaded_file": content_image}
#         content_res = requests.post(f"http://127.0.0.1:8000/content", files=content_file)
#         st.text("Content Photo:")
#         st.image(content_image, width=500)
#     else:
#         st.text("You haven't uploaded a content photo")
#         flag = False
    
#     if style_image is not None:
#         style_file = {"style_file": style_image}
#         style_res = requests.post(f"http://127.0.0.1:8000/style", files=style_file)
#         st.text("Style Photo:")
#         st.image(style_image, width=500)
#     else:
#         st.text("You haven't uploaded a style photo")
#         flag = False
    
#     if flag == True:
#         st.text("If you are happy with the photos, hit MASH")
