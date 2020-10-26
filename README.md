# SMB-datatool

inkscape is used to create the figures


WHEN DEPLOYING TO A VPS VM:
* clone the repo and run setup.bash
* create an empty db.sqlite3 under the site_SMB folder to store user credentials (note that this database setup is for testing only, for deployment, a proper database should be used, such mongodb on azure)
* add vm external ip to django allowed host in site\_SMB/settings.py
* allow 8000 port traffic in vm settings
* the secret key in site_smb/site_smb/setting.py is left blank, run following command on your linux terminal to get a new secret_key to fill in the setting file. 
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' 
```


DEVELOPMENT NOTE:
* for forms submission to work for visits from mac, csrf needs to be in the form body using {% csrf_token %}. puting csrf in ajax header doesn't work.


