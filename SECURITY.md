# Security

# Client <> Server Communication

⚠️ We do as of right now do not communicate via https.

# Authentication / User Identification

We use JsonWebToken to identify users that have authenticated with email and password.

The jwts are generated with the HS256 algorithm.

⚠️ the HS algorithms are not secure, they can be brute forced

# Storing Passwords

We hash the given plain text emails and passwords of each user with the md5 algorithm and store the hash.
A user logging in has to match the email and password in hashed form.

⚠️ md5 is not a secure hashing algorithm, they can be brute forced

# Storing JWTs (client side)

We do not store the JWT yet.

# Authentication Token Lifetime

The authentication cookie life has two levels. The cookie itself has a lifetime and is rejected after that lifetime.
This prevents old JWTs from accessing data that they are not supposed to attacks.

⚠️ The JWT has currently no life time.

The other level is the cookie life time in the browser. Since the auth token is set as a Http-Only Secure cookie. Users
and attackers are not be able to access them via the browser. The cookie has a life time set to 3 hours and any user
logged out for more then 3 hours will loose the cookie and has to log in again.
Every request with a valid cookie will refresh the cookies value and gives the user another 3 hours until the cookie
expires in the browser.

# UX

⚠️ We have no way to change the account password via the web-interface.
