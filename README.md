# SMB-datatool

inkscape is used to create the figures


WHEN DEPLOYING TO A VPS VM:
`clone the repo and run setup.bash
`create an empty db.sqlite3 under the site_SMB folder to store user credentials (note that this database setup is for testing only, for deployment, a proper database should be used, such mongodb on azure)
`add vm external ip to django allowed host in site\_SMB/settings.py
`allow 8000 port traffic in vm settings

DEVELOPMENT NOTE:
for forms submission to work for visits from mac, csrf needs to be in the form body using {% csrf_token %}. puting csrf in ajax header doesn't work.


