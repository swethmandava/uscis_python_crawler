# USCIS Python Crawler
If you're here - I'm sorry you have to deal with this! I'm rooting for you :)

It's just a simple [USCIS](https://egov.uscis.gov/casestatus/mycasestatus.do) crawler to analyze receipt numbers close to yours.


## Python installation for local development

```
pip3 install virtualenv
virtualenv -p /usr/bin/python3 uscic_crawler_venv
source uscic_crawler_venv/bin/activate
pip3 install -r requirements.txt
pip3 install -e .
```

## Running the crawler

```
python crawl_uscis --receipt_prefix=<3 letter string> --receipt_number=[<10 digit number>, <10 digit number>, ..] --crawl_range=<int correlating to paranoia level>
```


### Sample Output

```

Your Summary:

Description: On June 4, 2021, we received your Form I-765, Application for Employment Authorization, Receipt Number WAC2124651376, and sent you the receipt notice that describes how we will process your case.  Please follow the instructions in the notice.  If you have any questions, contact the USCIS Contact Center at www.uscis.gov/contactcenter.  If you move, go to www.uscis.gov/addresschange to give us your new mailing address.
Title: Case Was Received

Description: On June 4, 2021, we received your Form I-130, Application for Employment Authorization, Receipt Number WAC2124651376, and sent you the receipt notice that describes how we will process your case.  Please follow the instructions in the notice.  If you have any questions, contact the USCIS Contact Center at www.uscis.gov/contactcenter.  If you move, go to www.uscis.gov/addresschange to give us your new mailing address.
Title: Case Was Received

Description: On June 4, 2021, we received your Form I-485, Application for Employment Authorization, Receipt Number WAC2124651376, and sent you the receipt notice that describes how we will process your case.  Please follow the instructions in the notice.  If you have any questions, contact the USCIS Contact Center at www.uscis.gov/contactcenter.  If you move, go to www.uscis.gov/addresschange to give us your new mailing address.
Title: Case Was Received

Analyzing neighbors:

Stats from Before your receipt number
Approved:27/49
RFE:4/49
Received:18/49
Other:0/49

Stats from After your receipt number
Approved:25/51
RFE:4/51
Received:21/51
Other:1/51

Your Neighbors summary stored to uscis_crawls.json
```

## TODO

Wanna make a cron job? Send yourself an email? Feel free to push to this repo!
