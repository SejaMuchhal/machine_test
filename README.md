# Test Submission for Python - Django Developer position

## API Documentation
-----------------

### Insomnia collection : https://github.com/SejaMuchhal/machine_test/tree/master/API_Documentation
#### Export format - Insomnia v4(JSON)

## i. User - Registration
### Create/ Register a new user.

* #### Endpoint 	: /registration/

* #### Request Type 	: POST

* #### Request Params 	: **Required** - username, password, password_2,
 #### **Optional** -email,first_name, last_name
* #### Response 	: 
     ~~~ 
     { "token": <token> }
     ~~~

* #### Response Http status codes : HTTP_200_OK or HTTP_400_BAD_REQUEST

## Request Sample

```
{
 "username":"testuser",
 "password1":"testpassword",
	"password2":"testpassword"
}

```
## Response Sample

```
{
  "key": "78064bd87ed2073114cd7675af9196599b7c048c"
}
```


# ii. User - Login

## Obtain authentication token given the user credentials
### Token can be used to uniquely identify a user

* #### Endpoint 	: /login/

* #### Request Type 	: POST

* #### Request Params 	: username and password 
  #### "Must include username and password"
* #### Response 	: 
     ~~~ 
     { "token": <token> }
     ~~~

* #### Response Http status codes : HTTP_200_OK or HTTP_400_BAD_REQUEST

## Request Sample

```
{
	  "username": "seja",
    "password": "12345678"
}

```
## Response Sample

```
{
  "key": "79bc69481ba858c781071ba030a6b5018aa25add"
}
```

	
## iii. Get Post List

### Paginated list of posts

* #### Endpoint 	: /api/get_posts

* #### Request Type 	: POST

* #### Request Params 	: page *(Required)*

* #### Response Http status codes : HTTP_200_OK or HTTP_400_BAD_REQUEST

## Description

> Post list will be ordered according to previously liked posts and hence respective tags.Post with most liked tags will be at top similiarly post with most disliked tag will be at bottom. Append site domain to Image url to access images of post. For exampe 127.0.0.1:8000/media/images/dimitry-zub-9cMfke5bgnY-unsplash.jpg.

## Request Sample

```
{
  "page":1
}
```
## Need to include the token in the header of request.
~~~
Content-Type: application/json
Authorization: Token 79bc69481ba858c781071ba030a6b5018aa25add
~~~

## Response Sample

```
{
  "data": [
    {
      "post_id": "403c011c-f872-411f-87d7-bd898477378a",
      "description": "Third test post",
      "images": [
        "/media/images/dimitry-zub-9cMfke5bgnY-unsplash.jpg",
        "/media/images/michal-hlavac-4KUOtE_1_N8-unsplash_RBGHO86.jpg",
        "/media/images/dimitry-zub-9cMfke5bgnY-unsplash_LGFDKqo.jpg",
        "/media/images/matheo-jbt-nKcYv9GTvd8-unsplash.jpg"
      ],
      "status": "liked",
      "like_count": 1,
      "dislike_count": 0,
      "created_on": "2021-01-18"
    },
    {
      "post_id": "43bc4c9c-b672-4188-88d8-3e6f6f174d65",
      "description": "first test post",
      "images": [
        "/media/images/michal-hlavac-4KUOtE_1_N8-unsplash_lXdkQu3.jpg",
        "/media/images/hamish-weir-4CmUtT5KzQQ-unsplash.jpg",
        "/media/images/matheo-jbt-nKcYv9GTvd8-unsplash_AIvx2hL.jpg",
        "/media/images/tim-russmann-AnUdvJmrzOA-unsplash_KbNVDpj.jpg"
      ],
      "status": "liked",
      "like_count": 1,
      "dislike_count": 0,
      "created_on": "2021-01-18"
    }

  ]
}
```

## iv. Like/ Dislike Post

### API for liking and disliking a post
* #### Endpoint 	: /post_reaction
* #### Request Type 	: POST
* #### Request Params 	: reaction, post_id
* #### Response Http status codes : HTTP_200_OK or HTTP_400_BAD_REQUEST
  
## Description
| Param  | value for like | value for dislike    |
| ------------- |:-------------:|:--------------|  
| reaction      | 1     |     2          |

> If reaction is valid then returns status = True. If user has already liked/disliked post returns status = False. Value other than 1 and 2 for reaction will raise invalid request error. 
## Need to include the token in the header of request.
### Sample : 
```
Content-Type: application/json
Authorization: Token 79bc69481ba858c781071ba030a6b5018aa25add
```
## Request Sample : 
```
{
 "reaction":1,
 "post_id": "48464a48-8d0b-48b7-aa0d-1884dea069f5"
}
```

## Response Sample : 
```
{
  "status_code": 200,
  "status": true,
  "message": "Post liked successfully"
}
```

## v. Liked users list

## Paginated list of users who liked post

* #### Endpoint 	: /liked_userslist

* #### Request Type 	: POST

* #### Request Params 	: post_id[ type: string, format: uuid ],page [type: number]

* #### Response Http status codes : HTTP_200_OK or HTTP_400_BAD_REQUEST

## Description

> If post id is valid and post with that post id exists in database then it will return list of users who liked post. Users list will be ordered according to time they liked post, user who liked post latest will be at top of list and vice versa.Default page size is 5 i.e. max 5 users per page.

## Need to include the token in the header of request
### Sample : 
~~~
Content-Type: application/json
Authorization: Token 79bc69481ba858c781071ba030a6b5018aa25add
~~~
## Request Sample

```
{
  "post_id": "48464a48-8d0b-48b7-aa0d-1884dea069f5",
  "page": 1
}
```
## Response Sample

```
{
  "data": [
    {
      "user_id": "5a93abfb-e6ea-4a77-b464-82bb9df3407f",
      "username": "seja",
      "email": "seja@gmail.com"
    },
    {
      "user_id": "741a11f9-76fa-497f-acc4-0f27fa87e2b0",
      "username": "seja1",
      "email": "seja1@mail.com"
    },
    {
      "user_id": "af1e301b-567b-44c6-a257-edd397789f69",
      "username": "seja2",
      "email": "seja2@mail.com"
    }
  ]
}
```

# ---------
	
