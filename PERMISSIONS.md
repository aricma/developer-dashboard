# Permissions

In this file we will talk about the possible permissions, how they are handled, and who can give permissions to whom?

The following given problems need to be solved.
1. What permissions are there to begin with?
2. Who has which permissions?
3. Who can give permissions?
4. No one should get permissions per default that give them more rights than what they need.

The following use cases need to be covered.
1. We set up the app with no accounts and no permissions. The first account is created via the api.
2. The first account ...

To solve the issues we take as first step the way of the least privilege and least amount of work.
1. The admin of the software is the developer setting up the software. Accounts can be managed in the `accounts.yml` file.
2. All accounts created via the web interface are created with the right to read their own account per default.
3. Permissions can be given by accounts with the rights to write other accounts.
