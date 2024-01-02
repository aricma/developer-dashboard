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

# UX

⚠️ We have no way to change the account password via the web-interface.
