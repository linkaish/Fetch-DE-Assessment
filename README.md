# Fetch-DE-Assessment

## Steps
1. Pull docker images by running ```docker pull fetchdocker/data-takehome-localstack``` and ```docker pull fetchdocker/data-takehome-postgres```.
2. Run ```docker run -it -v shared-volume:/shared-data fetchdocker/data-takehome-localstack``` and ```docker run -it -v shared-volume:/shared-data fetchdocker/data-takehome-postgres``` to obtain ```container1``` and ```container2``` respectively, and create a shared volume for sharing files between two containers.
3. Run ```docker exec -it <container1_name> /bin/bash``` to enter the bash window in container1.
4. In container1, run code snippets ```apt-get install jq``` and ```chmod u+x extract.sh```, and upload files ```extract.sh``` and ```clean.py```.
5. Run ```./extract.sh``` to obtain all messages from AWS SQS Queue
6. Run ```pip install pandas``` and ```pip install pycryptodome```.
7. Run ```python clean.py``` to mask users' ip address and device id and obtain a new cleaned file called ```masked_user_logins.csv```.
8. Press Ctrl + D to exit container1.
9. Run ```docker exec priceless_blackwell sh -c 'echo "masked_user_logins.csv" > /shared-data/masked_user_logins.csv'``` to pass the cleaned file to the shared volume.
10. Run ```docker exec -it <container2_name> /bin/bash``` to enter the bash window in container2.
11. In container2, run ```psql -d postgres -U postgres -p 5432 -h localhost -W``` and enter password ```postgres```.
12. In postgres, run
```
COPY user_logins(user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
FROM '/shared-data/masked_user_logins.csv'
DELIMITER ',' 
CSV HEADER;
```
to load the CSV file into database.


## Questions
● How would you deploy this application in production?
  1. Build the whole ETL procedure as a deployment, such as a Docker image or Prefect deployment.
  2. Employ staging and production environments to test and deploy.
     
● What other components would you want to add to make this production ready?
  Implement monitoring solutions to track the health and performance of the ETL application and set up alerts.
  
● How can this application scale with a growing dataset.
  We can automate the ETL application when new data come in and use Spark to handle high volume data.
  
● How can PII be recovered later on?
  We can use the same encryption key to decrypt. I include a decrypting function in clean.py for reference.
  
● What are the assumptions you made?
  I assume we have a reliable data source and there is no conflict between the ETL and other applications.
