# BranchChat
Branch support chat application

To run locally:
- Clone repo
- Add SECRET_KEY and DEBUG environment variables
- Install required packages from Pipfile or requirements.txt in local environment
- Run `docker run -p 6379:6379 -d redis:2.8``(requires Docker)
- Run `python manage.py runserver`
- Access http://127.0.0.1:8000
