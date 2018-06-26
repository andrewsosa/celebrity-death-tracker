FROM python:3.6

# Configure
EXPOSE 80
WORKDIR /nltk-service

# Add our language service
ADD ./nltk-service requirements.txt ./

# Install requirements
RUN pip3 install -r requirements.txt
RUN [ "python", "-c", "import nltk; nltk.download('all')" ]

# Set our deployment
CMD [ "nameko", "run",  "--config", "config.yaml", "__init__"]
