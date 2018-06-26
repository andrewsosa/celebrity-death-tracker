FROM python:3.6

# Configure
EXPOSE 80

# Add our language service
ADD ./nltk-service requirements.txt /nltk-service/

# Install requirements
RUN pip3 install -r /nltk-service/requirements.txt
RUN python /nltk-service/install_nltk.py

# Set our deployment
CMD [ "nameko", "run",  "--config", "/nltk-service/config.yaml", "nltk-service"]
