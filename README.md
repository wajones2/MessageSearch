# MessageSearch

MessageSearch is a Command-Line Interface program that allows users to explore the Messages application database on a MacBook.

# Configuration

MessageSearch utilizes two databases: contacts.db and chat.db (Messages app database). 

1. Execute ```./config``` to create the contacts database, copy the Messages database to the program directory, and fill the contacts database with the info of any phone number that has been messaged as long as it is a saved contact.

# Operation

Once Python is running in the command-line:

2.  Import the library with 
```
>>> from xapp import *
```
3.  Search for messages with 
```
>>> xm.message_search('CONTACT NAME HERE', 'KEYWORDS TO SEARCH HERE')
``` 

If more than one contact with the same name exists, an option to select the intended contact will print. For example:

```
>>> xm.message_search('Jane', 'birthday')
```

output

```
Enter contact #:

[1] Jane Doe
[2] Jane Austen

```

After the number of the desired contact is entered, each message will display a formatted timestamp after a color-coded bullet point - green for sent, red for received - with the message on the next line.

Enjoy!
