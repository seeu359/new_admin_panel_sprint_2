from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()


include(
    'components/base.py',
    'components/application.py',
    'components/database.py',
    'components/localization.py',
    'components/media.py',
)


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
