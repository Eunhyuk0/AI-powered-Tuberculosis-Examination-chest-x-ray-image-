# AI-powered-Tuberculosis-Examination-chest-x-ray-image-
Express node js code runs FastAPI python code, train an Keras AI model using aimodel.py

**Basic idea :**
we sometimes have to get chest x-ray examination for school dormitory, millitary application, etc.
they would call a doctor with a chest x-ray device.
purpose of this project is to automate this process to contain cost and apply AI to medical services.

*comments are in Korean for submission to my school*

to run each code, navigate to the directory (run cmd on vs code or use "cd" command)
and "uvicorn api:app --reload" and "node APIMidware.js" in 2 different cmd windows

it will run python FastAPI backend and server itself(node.js) on your pc. you can access the web page only through localhost.
the html code was developed with ChatGPT (I hate HTML/CSS literally)
for AI model, I searched for tuberculosis / normal chest X-ray images on Kaggle but couldn't find a large dataset.
used a simple, shallow Keras model for binary classifying.
