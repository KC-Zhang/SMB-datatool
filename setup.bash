# add server ip to settings.py, i.e ALLOWED_HOSTS = ['34.92.69.244']
# run server with python3 site_SMB/manage.py runserver 0.0.0.0:8000

sudo apt update
sudo apt install python3-pip
alias python=python3
alias pip=pip3
python -m pip install Django
pip install pandas
pip install xlrd
pip install openpyxl
pip install XlsxWriter
pip install django-cleanup

# for making icons
sudo snap install inkscape

# for converting downloaded html landing page to django template
#regex search: =("|')(.+?)(?<=tony-ai-1)  #change tony-ai-1 accordingly
#regex replace: =$1./landingPage_files
#replace //(.+?)(?<=tony-ai-1)
# by ./landingPage_files
#replace (src|href)="(?!(http|#))(.+?)(?<!html)"
#by $1="{% static '$3' %}"
#replace (url\()(.+?)(\))
#by $1{% static '$2' %}$3


