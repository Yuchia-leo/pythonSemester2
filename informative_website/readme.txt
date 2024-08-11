Here is a introduction for this website:

Data:
    The data in this website is of three kinds:
        - csv: These are data for making informative graphes. The source is https://www.oecd.org/climate-action/ipac/dashboard?country=ARG
        - forum data: Topics and comments produced by users in forum.
        - tracking data: Information on people's visit within the website.

DataCleaning:
    The codes to clean data is in the end of ghg.sql 
    How I clean:
        - I only kept the data only from 2000 to 2021
        - I gather key data from each table into one table and The columns where these data are stored form foreign key relationships with the columns in the original table.


Database:
    - The database used for keeping data from those csv files which are used for making informative graphes is ghg.db and ghg.sql is the sql syntax to operate the database.
        Within ghg.sql, it includes my data cleaning operations.
    - forum.db is the database to store the topics and comments in the forum and forum.sql is the sql syntax to operate it.
    - track.db is the database to store information of user tracking and track.sql is the sql to it.

Backend Files(Python):
    - app.py: used to set up this app incluing every pages in it.
    - db.py: oprations I created to control databases easier.
    - email_util.py: used for resetting users' passwords.
    - forum_db.py: codes I created to do operations in the forum easier. 
    - graphes.py: codes to make informative graphes.
    - password_util.py: used to create and check users' passwords.

Email
    - use smtplib (based on Simple Mail Transfer Protocol)
        - https://docs.python.org/3.2/library/smtplib.html
    - https://realpython.com/python-send-email/
        - 2 ways
            - sending email to a public email server requires authentication (login, password for the `from` email)
            - sending email to a local email server - doesn't require authentication
    - choose Option 2 (local email server)
        - need to start email server
            - use aiosmtpd
                - install it
                    pip install aiosmtpd
                
                - start mail server
                    C:\Users\pingl>aiosmtpd -l localhost:1025 -n
        - use local email server
            - means to send email to local email server
                - therefore, not expect to receive real email like gmail
                - but check output of local email server, the output is a kind of email as below

                    ---------- MESSAGE FOLLOWS ----------
                    Subject: forgot password
                    From: admin
                    To: z@z
                    Content-Type: text/plain; charset="utf-8"
                    Content-Transfer-Encoding: 7bit
                    MIME-Version: 1.0
                    X-Peer: ('::1', 63517, 0, 0)

                    temporary password: da5178ca5fb24bae8d729e5c02eee56e
                    ------------ END MESSAGE ------------

How to change password?
    - make sure local email server (aiosmtpd) is started and running as above

    - Sign in -> Forgot password? -> enter Email -> Forgot Password page

    -> then go to command line console to get aiosmtpd SMTP server's email output as follows

        ---------- MESSAGE FOLLOWS ----------
        Subject: forgot password
        From: admin
        To: z@z
        Content-Type: text/plain; charset="utf-8"
        Content-Transfer-Encoding: 7bit
        MIME-Version: 1.0
        X-Peer: ('::1', 63517, 0, 0)

        temporary password: da5178ca5fb24bae8d729e5c02eee56e
        ------------ END MESSAGE ------------

    -> copy temporary password: da5178ca5fb24bae8d729e5c02eee56e to Forgot Password page
    -> continue on Reset Password

In the forum, if user have the admin code which is 14806762, he can register as an admin. 
An admin has the right to make topics which is ideas about GHG emission protection 
and delete improper comments.

