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
Load into pandas -> convert to Mysql database -> this is done via createsqldb.py

Step 1
```
python scrapeNBA.py /path/to/directory_to_place_raws
```
Output: Saves a directory of the date of the scrape in the output directory. Raw text files are stored.

Step2:
```
python datacleanup.py /path/to/directory_to_place_raws
```
Output: Saves a directory of the date of the scrape in the `cleaned` directory with the cleaned tables

Step3:
```
python createsqldb.py /path/of/cleaned/tables
```
Output: saves out to `sqldb` directory of the MySQL dump file created via the raw tables.

Step4: upload the sql dump files onto google bucket of choice and host.

# Connection Address:
bmi520nbastatssql:us-central1:nbastatsscrape
IP:
34.27.167.16
email:
p641611893501-xouqgc@gcp-sa-cloud-sql.iam.gserviceaccount.com

# ipynb file is the analysis done via the SQL server.
Will be offline because it costs money to have online unless specified.


# run into gcloud instance

```gcloud compute ssh --zone "us-west4-b" "instance-20240428-165238" --project "bmi520nbastatssql"```



