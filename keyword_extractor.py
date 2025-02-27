from google import genai
import spacy
import numpy
from pypdf import PdfReader

def readpdf(pdf):
    reader = PdfReader(pdf)
    page = reader.pages[0]
    text = page.extract_text()
    return text

def rate_resume(text,description):

    ner = spacy.load("en_core_web_lg")

    entities = ner(text)
    
    keywords = numpy.array([])
    
    for entity in entities.ents:
        print(entity.label_)
        if entity.label_ == "WORK_OF_ART":
           keywords = numpy.append(keywords,(entity.text).lower())
    
    for entity in entities:
        if entity.pos_ == "NOUN" or entity.pos_ == "PROPN" :
           keywords = numpy.append(keywords,(entity.text).lower())
    
    client = genai.Client(api_key="AIzaSyD0I7tw8w9wo3c7BFebS9PeJimi_GJWkT0")
    
    response = client.models.generate_content(model = "gemini-2.0-flash",contents=[f"just write the name of all the technical skills and one or two other general skills and the educational qualifications present in {description} wihout any paranthesis seperated with comma and just take the words as they are dont change them"])
    mentioned_skills = (str(response.text).lower()).split(",")
    
    mentioned = []
    for skill in mentioned_skills:
        mentioned.append(skill.strip()) 
    
    common_keywords = list(set(keywords) & set(mentioned))
    skills_not_found = list(set(mentioned) - set(keywords))
    
    score = int(len(common_keywords)/len(mentioned) *100)
    return(score,skills_not_found)
