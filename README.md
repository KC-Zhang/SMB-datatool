# SMB-datatool

inkscape is used to create the figures


WHEN DEPLOYING TO A VPS VM:
`add vm external ip to django allowed host in site\_SMB/settings.py
`allow 8000 port traffic in vm settings

DEVELOPMENT NOTE:
for forms submission to work for visits from mac, csrf needs to be in the form body using {% csrf_token %}. puting csrf in ajax header doesn't work.

