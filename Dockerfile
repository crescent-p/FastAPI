FROM python:3.9.7

#changes the dir to this
WORKDIR /usr/src/app

#to optimise for docker caching. if requirements didnt change then the dockerfile woudlnt be rebuild

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

#copy all source files from current directory to image
COPY . .

#any command you wanna run, put it inside CMD, spaces = new word, weird.

CMD [ "uvicorn", "apps.main:app", "--host", "0.0.0.0", "--port", "8000" ]

#To build the image
#docker build -t <nameOfImage> <whereTheDockerFileis>