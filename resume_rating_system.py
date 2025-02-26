import streamlit as st
from pypdf import PdfReader 
from keyword_extractor import rate_resume

st.set_page_config(layout = "wide")

st.title("Resume Rating System")

resumes = st.file_uploader("upload your resume",type = "pdf",accept_multiple_files = True)
min_score = st.text_input("Enter Minimum score:, (on a scale of 0 to 100")
if type(min_score) == float or int:
    
    resume_text = {}
    
    if len(resumes) > 0:
        for resume in resumes:
            reader = PdfReader(resume)
            page = reader.pages[0]
            text = page.extract_text()
            resume_text[resume.name] = text
            
    description = st.text_input("Enter description:")
    
    for resume in resume_text:
        score,skills_not_found = rate_resume(str(resume_text[resume]),description)
        resume_text[resume] = [resume_text[resume], str(score),str(skills_not_found)]  
    
    sorted_resumes = sorted(resume_text,key = lambda x: x[1])
    
    seleted_resumes = 0
    
    done = False
    if min_score.strip() != "":
        if description.strip() != "":
           st.write("Filtered resumes according to score : ")
           for sr in sorted_resumes:
               if resume_text[sr][1] > min_score:
                   st.code(sr + " : " + resume_text[sr][1])
                   seleted_resumes += 1
               if sr == sorted_resumes[-1]: 
                  done = True
        else:
            st.write("please provide a description")
    else:
        st.write("please enter minimun score to get filtered resumes")

    if done == True and seleted_resumes == 0:
       st.code("All resume scored below than required score")
        
    st.write("\n\n\n")
    
    if description.strip() != "":   
        st.write("All resume with scores: ")
        for res in resume_text:
            st.code(f"Name: {res} \nscore : {resume_text[res][1]}\nskills not found : {(resume_text[res][2])}")

else:
    st.header("Make sure the minimun score is a number")
