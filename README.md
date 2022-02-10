about
-----

The user writes a ticket and sends it, the support reviews and answers it,
when solving the ticket, indicates the status is "resolved"

Endpoints
---------

/auth/users/	    -Register new user
/auth/users/me/	    -get/update registered user
/auth/jwt/create/	-create a JWT by passing the valid user in the request
                     post this endpoint
/auth/jwt/refresh/	-get new JWT after lifetime expired earlier
                     generated
/api/profiles/	    -get all user profiles and create a new one
/api/profile/id/	-user profile detail view
/api/tickets        -CRUD tickets
/api/answers        -CRUD answers(to write the answer you need to specify the 
                     parent)

start: docker-compose up --build
