# TRUECALLER API CLONE

A clone of Truecaller API, built using Flask Framework.  
To see the instructions on how to run this API, click [here](instructions.txt)

## API functionalities

**Note**: Authorization header required for all operations
- Register/Create Account
- Login
- Add contact
- Mark number as spam
- Search contact by name
- Search contact by phone number

## HOME PAGE

Asks the user to register/login if not logged in, i.e., no valid authorization Token was passed by the user while sending this request.  
Notice the empty Key-Value pair in the Headers section.

<img width="1392" alt="Screenshot 2022-08-24 at 8 08 47 PM" src="https://user-images.githubusercontent.com/15028913/186447126-a1c31d2c-6f85-4c0c-a9b7-e71643ba0b3c.png">

## REGISTRATION PAGE

- Takes details of the new user  
- Creates new user  
- Asks them to go to /login  

### User 1
<img width="1392" alt="Screenshot 2022-08-24 at 8 11 50 PM" src="https://user-images.githubusercontent.com/15028913/186447895-bd0310a7-8645-4498-a348-a4843cc5299d.png">

### User 2
<img width="1392" alt="Screenshot 2022-08-24 at 8 12 36 PM" src="https://user-images.githubusercontent.com/15028913/186448105-d25e2cda-0be6-4e8c-a391-f112350368a8.png">

## LOGIN PAGE

Takes username and password to check for a valid user.  
Only then will it add/sync contacts provided by the user.

Also generates a unique Authentication Token which is shown to the user as it would be needed to be entered for further requests by the user to validate whether he is logged in or not (refer [instructions.txt](instructions.txt) to see how to pass this auth_token) 

### User 1
<img width="1392" alt="Screenshot 2022-08-24 at 8 14 23 PM" src="https://user-images.githubusercontent.com/15028913/186448556-8ff4e158-3e59-45bb-bd18-2619d0e2fa68.png">

### User 2
<img width="1392" alt="Screenshot 2022-08-24 at 8 15 05 PM" src="https://user-images.githubusercontent.com/15028913/186448738-7d578468-f08b-4f73-9c17-097800699269.png">

Notice that both the users have diffeAent authorization Tokens. Whichever authorization Token is passed along with the request, the request would be by that specific user.

## ADD CONTACTS

### User 1
We have provided the Authorization Token for User 1 in the Headers section.  
<img width="1271" alt="Screenshot 2022-08-24 at 8 22 18 PM" src="https://user-images.githubusercontent.com/15028913/186450588-fe190751-4a25-4fc2-8f69-5588b7f629fb.png">

Our Body has the contacts of User 1 that are to be added  
<img width="1392" alt="Screenshot 2022-08-24 at 8 22 56 PM" src="https://user-images.githubusercontent.com/15028913/186450736-b426ae4c-057e-419c-af57-6716d0891450.png">

### User 2
We have provided the Authorization Token for User 2 in the Headers section.  
<img width="1271" alt="Screenshot 2022-08-24 at 8 24 48 PM" src="https://user-images.githubusercontent.com/15028913/186451176-0cea56a3-c13e-4b2f-9e64-49f59370d988.png">

Our Body has the contacts of User 2 that are to be added  
<img width="1392" alt="Screenshot 2022-08-24 at 8 31 30 PM" src="https://user-images.githubusercontent.com/15028913/186452914-4fd42348-d60e-4aaf-b025-115822663289.png">

User 1 has 3 contacts and User 2 has 4 contacts  
User 2 has same 3 phone numbers as User 1 but with different names and he also has the phone number of User 1 

## Current State of Database

### User table
<img width="1172" alt="Screenshot 2022-08-24 at 8 33 59 PM" src="https://user-images.githubusercontent.com/15028913/186453538-5ca14b0b-790a-4e01-bed7-00af422f29bc.png">

### Contact Table
<img width="1172" alt="Screenshot 2022-08-24 at 8 33 42 PM" src="https://user-images.githubusercontent.com/15028913/186453481-47229e01-d64f-4051-9c7e-3bcaf173f500.png">

## SEARCH BY NAME

A user can search for a person by name in the global database. Search results display the name, phone number and spam likelihood for each result matching that name.

We have provided the Authorization Token for User 1  
See the Key-Value pair inside Headers

### Search 1
<img width="1270" alt="Screenshot 2022-08-24 at 8 38 38 PM" src="https://user-images.githubusercontent.com/15028913/186454695-4970798d-928b-45c4-9687-40637a7bc461.png">

### Search 2
<img width="1270" alt="Screenshot 2022-08-24 at 8 39 59 PM" src="https://user-images.githubusercontent.com/15028913/186455000-2dbc1a11-9565-4dc4-9c48-4ccefb80e138.png">

## SEARCH BY NUMBER 

A user can search for a person by phone number in the global database. If there is a registered user with that phone number, show only that result. Otherwise, show all results matching that phone number completely - note that there can be multiple names for a particular phone number in the global database, since contact books of multiple registered users may have different names for the same phone number.

We have provided the Authorization Token for User 2
See the Key-Value pair inside Headers

### Not a registered User
<img width="1270" alt="Screenshot 2022-08-24 at 8 43 07 PM" src="https://user-images.githubusercontent.com/15028913/186455682-255e11e5-7392-4e7f-a106-9200279a7b05.png">

### Registered User
<img width="1270" alt="Screenshot 2022-08-24 at 8 46 21 PM" src="https://user-images.githubusercontent.com/15028913/186456440-dc2efa1e-70fa-4110-9ebd-87c43f6f30c3.png">

## CHANGING SPAM STATUS

A user should be able to mark a number as spam so that other users can identify spammers via the global database. Any registered user can change the spam status for any number in the global database.  
**Note** : It isn't necessary that the number should belong to any registered user or contact - it could be a random number.

We have provided the Authorization Token for User 2
See the Key-Value pair inside Headers

<img width="1270" alt="Screenshot 2022-08-24 at 8 57 21 PM" src="https://user-images.githubusercontent.com/15028913/186459000-b0bec3e0-f1da-4855-844b-1fa7836a5511.png">

Notice that the number was saved by both our registered users, but with different names and even though User 2 changed the spam status, it has changed for both the registered users.

### Searching for the same number now shows the changed status for that number

<img width="1270" alt="Screenshot 2022-08-24 at 9 02 22 PM" src="https://user-images.githubusercontent.com/15028913/186460173-621cbf20-4df4-4271-9f43-8df027a2cd57.png">

### Database after changing spam status

### Contact Table
<img width="1168" alt="Screenshot 2022-08-24 at 9 03 54 PM" src="https://user-images.githubusercontent.com/15028913/186460489-84d07a7d-ef97-42cd-9f1e-25a851669299.png">

## LOGOUT

User 2 is logging out.  
We have provided the Authorization Token for User 2. See the Key-Value pair inside Headers.

<img width="1276" alt="Screenshot 2022-08-24 at 9 25 29 PM" src="https://user-images.githubusercontent.com/15028913/186465285-2a2c8e79-3ed6-4269-b32a-c580d8d48204.png">

As soon as User 2 logged out, notice that the database column having the Authorization Token for User2 is set to null, which indicates he is not in session anymore.  

<img width="1167" alt="Screenshot 2022-08-24 at 9 26 49 PM" src="https://user-images.githubusercontent.com/15028913/186465626-7ace4785-73fe-400b-bac9-b133d880d5f2.png">

Now, even if we pass the earlier Authorization Token for our requests, it would ask to sign in first.
Would also ask to sign in if we don’t pass any Authorization Token.