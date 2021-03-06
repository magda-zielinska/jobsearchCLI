# jobsearchCLI
a CLI for searching and saving links to job listings

It will find up to 26 links to job ads and save them to a csv 'job_listings.csv'
on your Desktop, if you are running a Mac or Windows machine. For Linux users the file 
will be saved to the directory with the script.

Looking through job listings can sometimes be demotivating to say the least.
Why not just save a bunch of links to the job announcements, visit a specific ad directly and take it from there?

Me and my friends find it more convenient and stress reducing.

Download the geckdriver for Selenium from here:
https://github.com/mozilla/geckodriver/releases

Make sure it’s in your PATH, e. g., place it in /usr/bin or /usr/local/bin or directly
in the projects folder.

## Run it in a virtual environment Mac or Linux:

`python3 -m venv .venv`<br>
`. .venv/bin/activate`<br>
`pip install -r requirements.txt`<br>
`python3 jobsearch.py [JOB] [LOCATION] -options`<br>

## Run it in a virtual environment on Windows:

`python -m venv .venv` <br>
`.venv\Scripts\activate.bat`<br>
`pip install -r requirements.txt`<br>
`python jobsearch.py [JOB] [LOCATION] -option`<br>

## Usage
```
usage: jobsearch.py [-h] [-n NUMBER] [-s] [-l] [JOB [JOB ...]] LOCATION

tool to store links to job adds

positional arguments:
  JOB                   the position you are looking for
  LOCATION              the city in which you are looking for a job

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        number of links to be stored, max: 26
  -s, --stackoverflow   look for jobs on stackoverflow, default: linkedin
  -l, --linkedin        look for jobs on linkedin
```


