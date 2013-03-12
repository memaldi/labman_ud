Projects MORElab
================

Web app to manage project's data within the MORElab research group at deustotech.

In order to have the application fully running all the features correctly, the following parameters need to be filled:

    > projects_morelab/settings.py
    
    { ... }
    
    DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
      }
    }
    
    { ... }
    
    # Email settings to allow mail sending from a gmail account
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    DEFAULT_FROM_EMAIL = ''
    SERVER_EMAIL = ''
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    
    PROJECTS_RECEPTOR_EMAILS = ['']
    PROJECTS_SENDER_EMAIL = ''
    
# Database initialization
    
There are some fixtures existing inside each app. They can be uploaded when the database its created/updated by the following command from the root folder of the project:

    python manage.py syncdb
