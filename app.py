import streamlit as st 
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()  
from PIL import Image

genai.configure(api_key='AIzaSyAtdirs2MXnMC2Dm985ZKuja51_oOlc80g')

def get_gemini_response(input_prompt,image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input_prompt,image[0]]);
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        
        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Your Nutrition Tracker App!!") 

st.header("Your Nutrition Tracker App!!")
uploaded_file=st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image..", use_column_width=True)
    
submit=st.button("Tell me about the Nutritional content!!")

input_prompt="""
If the image uploaded is not of any food item respond as 'Please upload a valid image'.
You are an expert in nutritionist where you need to see the food items of the image and calculate
the total calories, also provide the details of every food items with the calorie intake 
in the below format:

1. Item 1 - no of calories
2. Item 2 - no of calories
----
----
Finally  mention the percentage split of the ratio of carbohydrates, fats, fibres,sugar and other things 
required in the diet and also mention whether the food if healthy or not.
"""

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data)
    st.header("The Nutritional and Calorie contents are ")
    st.write(response)
