# TRUECALLER API CLONE

A clone of Truecaller API, built using Flask Framework.  
To see the instructions on how to run this API, click [here](instructions.txt)

## API functionalities

**Note**: Authorization header required for all operations
- Create Account
- Add contact
- Mark number as spam
- Search contact by name
- Search contact by phone number

## HOME PAGE

Asks the user to register/login if not logged in, i.e., no valid authorization token was passed by the user while sending this request.  
Notice the empty Key-Value pair in the Headers section.

<img width="452" alt="image" src="https://user-images.githubusercontent.com/15028913/186335255-bcabe648-9b37-4f9b-992a-27d950102673.png">

## REGISTRATION PAGE

Takes details of the new user
Creates new user
And asks them to go to /login

### User 1
<img width="452" alt="image" src="https://user-images.githubusercontent.com/15028913/186335270-9474ff11-eaef-41ba-b470-317d94089331.png">

### User 2
<img width="452" alt="image" src="https://user-images.githubusercontent.com/15028913/186335328-44675326-02da-4130-9572-8ac8a0604d72.png">

## LOGIN PAGE

Takes username and password to check for a valid user.  
Only then will it add/sync contacts provided by the user.

Also generates a unique Authentication Token which is shown to the user as it would be needed to be entered for further requests by the user to validate whether he is logged in or not (refer [instructions.txt](instructions.txt) to see how to pass this auth_token) 

### User 1
<img width="452" alt="image" src="https://user-images.githubusercontent.com/15028913/186335301-32a5c166-70dd-4b91-8753-35425bbe129c.png">

### User 2
<img width="452" alt="image" src="https://user-images.githubusercontent.com/15028913/186335346-102b8127-c840-4e0c-ae2e-b735525e227e.png">

Notice that both the users have different authorization tokens. Whichever authorization token is passed along with the request, the request would be by that specific user.

User 1 has 3 contacts and User 2 has 4 contacts  
User 2 has same 3 phone numbers as User 1 but with different names and he also has the phone number of User 1 

## SEARCH BY NAME

A user can search for a person by name in the global database. Search results display the name, phone number and spam likelihood for each result matching that name.

We have provided the authorization token for User 2  
See the Key-Value pair inside Headers

### Search 1
<img width="452" alt="image" src="https://user-images.githubusercontent.com/15028913/186337399-24c4e5fc-2a46-4303-8f13-de2c45c7db24.png">

### Search 2
<img width="452" alt="image" src="https://user-images.githubusercontent.com/15028913/186337425-7f559c69-2119-43a5-819f-2789b32941e2.png">

## SEARCH BY NUMBER 

A user can search for a person by phone number in the global database. If there is a registered user with that phone number, show only that result. Otherwise, show all results matching that phone number completely - note that there can be multiple names for a particular phone number in the global database, since contact books of multiple registered users may have different names for the same phone number.

We have provided the authorization token for User 2
See the Key-Value pair inside Headers

### Not a registered User
<img width="452" alt="image" src="https://user-images.githubusercontent.com/15028913/186337835-a3626faa-b839-420e-bddc-57b6d9abe1b6.png">

### Registered User
<img width="452" alt="image" src="https://user-images.githubusercontent.com/15028913/186337847-19c79a22-9bb6-44b2-8f2c-a720e9cf4197.png">

## Changing Spam Status

A user should be able to mark a number as spam so that other users can identify spammers via the global database. Any registered user can change the spam status for any number in the global database.  
**Note** : It isn't necessary that the number should belong to any registered user or contact - it could be a random number.

We have provided the authorization token for User 2
See the Key-Value pair inside Headers

<img width="452" alt="image" src="https://user-images.githubusercontent.com/15028913/186339292-2cad509f-696b-4547-b172-ca309ccf1b3d.png">

Notice that the number was saved by both our registered users, but with different names and when User 2 changed the spam status, it has changed for both the users.

### Searching for the same number now shows the changed status for that number

<img width="452" alt="image" src="https://user-images.githubusercontent.com/15028913/186339823-675a257a-aa8d-4534-96fa-6cc4c5b9c465.png">

## CURRENT DATABASE

### User table
<img width="452" alt="image" src="https://user-images.githubusercontent.com/15028913/186339919-c13672a9-1dee-48bf-8edc-0a397d33d806.png">

### Contact Table
<img width="452" alt="image" src="https://user-images.githubusercontent.com/15028913/186339930-379b1e0c-1240-483e-a79b-7d0e40352474.png">

## LOGOUT

User 2 is logging out.  
We have provided the authorization token for User 2. See the Key-Value pair inside Headers.


<img width="452" alt="image" src="https://user-images.githubusercontent.com/15028913/186340067-36a715a9-e6b0-4966-9363-49c3591ff84a.png">

User 2 is logged out.

As soon as User 2 logged out, see that the database column having the authorization token for User2 is set to null, which means he is not in session anymore.  

<img width="452" alt="image" src="https://user-images.githubusercontent.com/15028913/186340120-b4146990-84e9-4ac5-8c8d-cd434293b8d4.png">

Now, even if we pass the earlier authorization token for our requests, it would ask to sign in first.
Would also ask to sign in if we don’t pass any Authorization token.