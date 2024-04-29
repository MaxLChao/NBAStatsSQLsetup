# BMI 520: Software Stacks

This is a git repo for Grabbing NBA Stats and generating a MYSQL database off of the webscraped data.
Data was scraped via Selenium off the nba web page, and then saved to the `raws` table folder. From there data is cleaned up to created readable tables and saved in the `cleaned` folder. 

Conversion of the data is done via a script to convert a directory of the tables with expected cleaned data and labels into a mysql database where each table can be linked via the ID and PLAYER columns. Upload of the data onto the Google Cloud instance was done via the GUI. SQL dump files were uploaded from the `sqldb` folder to a Google Bucket, which was then imported into the SQL server. The Free trial for google cloud was used to host the SQL server on a 64GB RAM, 8 Core server. 

Finally, basic analyses was done via querying the database on using physiological attributes like height, age, and wieght on basketball performance. The notebook has SQL commands using sqlalchemy to query the database, and from there to do downstream analysis.

The encompassing project with the notebook is included in the repo. Additional information about the project can be asked if needed. This was purely an academic project to learn:

1. How to webscrape 
2. Create a simple MYSQL database
3. Upload and manage a database on a cloud based server.
4. Access the database and query data to generate analyses. 


Basic premise is this:

- Grab NBA stats from webpages via selenium: grab text and tabular data
- Data clean
- Format data
- Create a SQL database (MySQL) housing this structure
- Upload onto Google Cloud SQL Server
- Analysis notebook querying the database to generate basic analyses of the variables




## Usage

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

Step5: Set up and activate the SQL server on cloud server.

Step6: Connect and run analysis. Ipynb has the steps that was run on google colab connected with my server account.

Step7: Analyze.

## Ipynb file is the analysis done via the SQL server.

**SQL Server will be offline because it costs money to have online unless specified.**

Will delete sometime this summer (2024) after trial ends.



