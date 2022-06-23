# Yatube API
### Yatube -- Social network
##### Description
Yatube is the network where people can share their diaries, read each other diaries, follow, comment, create communities. Users can choose their unique URL, can be blocked for spam, edit their posts.

### How to run the project:

Clone repository and go to it's derictory on your computer:
```
git clone https://github.com/loverazz/api_final_yatube.git
```
```
cd api_final_yatube
```

Create and activate virtual environment:

```
python -m venv env
```
```
source env/bin/activate
```
```
python -m pip install --upgrade pip
```

Install the requirements from requirements.txt:
```
pip install -r requirements.txt
```

Migrate:
```
python manage.py migrate
```

Run the project:
```
python manage.py runserver
```

### How to use Yatube API

All posts:
`api/v1/posts/`

Post details:
`api/v1/posts/{id}/`

All post comments:
`api/v1/posts/{post_id}/comments/`

Comment details:
`api/v1/posts/{post_id}/comments/{id}/`

All groups:
`api/v1/groups/`

Group details:
`api/v1/groups/{id}/`

Your followings:
`api/v1/follow/`

Get JWT-token:
`api/v1/jwt/create/`

Refresh JWT-token:
`api/v1/jwt/refresh/`

Verify JWT-token:
`api/v1/jwt/verify/`
