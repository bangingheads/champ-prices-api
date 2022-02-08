# Champion Prices API
 
Takes [Meraki champion data](http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions.json) and feeds it back as an API to use for champion store information.

## Running

### Uvicorn
You can run directly on your system using uvicorn
``
pip install -r requirements.txt
``
``
uvicorn app.main:app
``

### Docker
You can run it as a docker container
``
docker build -t meraki .
``
``
docker run -d --name meraki_champs -p 5555:80 meraki
``

