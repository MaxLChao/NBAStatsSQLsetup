## BMI 520: Software Stacks

Initial git repo for Grabbing NBA Stats with respect to physiological builds

Basic premise is this:

- Grab NBA stats from webpages via selenium: grab text and tabular data
- Data clean
- Format data
- Create a SQL database (PostGreSQL/MySQL) housing this structure
- Upload onto Google Cloud SQL Server
- Have script that can turn on/off Server
- Have script to query server and generate basic analyses

# Running

Use scrapeNBA.py to run the NBA scrape. 
files will be stored with current date in the raws directory in the tables dir. 

Use datacleanup.py to clean up data.
Files will be stored with directory name in cleaned

Final formatting before ingesting into a Database will occur in another script.
Load into pandas -> convert to Mysql database -> upload ont cloud is run via uploadupdates.py

