# mobile-gpt

## How to

1. Virtual Environment

Ensure python virtual environment is made using python3.6

2. Install packages

Install requirements with the command `python -m pip install -r requirements.txt`

Also, create a folder called `models` then unzip the `jokes.zip` file in google drive at that location

3. Set flask environment variables

Set flask app by `export FLASK_APP=run.py`

4. Running the flask app

To run command is `python -m flask run --host=0.0.0.0`

The host flag is necessary if running from Google Cloud Platform

5. Visit your external ip addess (running on GCP) or your localhost url


## API Mode

While the server is up, do `http://ipaddress:5000/generate_api?joke_title=title%3A+Why+did+the+chicken+cross+the+road?%3F`
Note: the payload must be url encoded

The response will look like this:
```
title: Why did the chicken cross the road? body: To get to the other side!
```
