from google import genai
import streamlit as st
import spacy
import numpy
from pypdf import PdfReader

def rate_resume(text,description):

    ner = spacy.load("en_core_web_lg")

    entities = ner(text)
    
    keywords = numpy.array([])
    
    for entity in entities.ents:
        if entity.label_ == "WORK_OF_ART":
           keywords = numpy.append(keywords,(entity.text).lower())
    
    for entity in entities:
        if entity.pos_ == "NOUN" or entity.pos_ == "PROPN" :
           keywords = numpy.append(keywords,(entity.text).lower())
    
    client = genai.Client(api_key=st.secrets["the_api_key"])
    
    response = client.models.generate_content(model = "gemini-2.0-flash",contents=[f"just write the name of all the technical skills that are present in {description} wihout any paranthesis seperated with comma"])
    mentioned_skills = (str(response.text).lower()).split(",")
    
    mentioned = []
    for skill in mentioned_skills:
        mentioned.append(skill.strip()) 
    
    common_keywords = list(set(keywords) & set(mentioned))
    skills_not_found = list(set(mentioned) - set(keywords))
    
    score = len(common_keywords)/len(mentioned)
    return (score,skills_not_found)
