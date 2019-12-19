#Big thanks to Yuji Tomita for this easy to implement solution.
#https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/
#Slightly modified by: Six-S

#NOTE: This is a quick, relatively hacky implementation of a simple email worker.
#I would like to build something more substantial, but this should be fine until I finish CodeBot itself.
#I plan on revisiting the email worker once CodeBot is in an okay state.

import imaplib
import email

    #### --------------- UTILITY FUNCTIONS --------------- ####

def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()

def save_to_file(body):
    if body:
        with open('challenge.txt', 'w') as open_file:
            open_file.write(body)

    #### --------------- CORE LOGIC --------------- ####

if __name__ in '__main__':

    error = False
    #there are plenty of situations that could cause this to fail.
    #If we fail, let's just put the error into our file so that our bot (or rather, our users) "know" about it.
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login('example@example.com', 'example')
        mail.list()
        # Out: list of "folders" aka labels in gmail.
        # connect to inbox here.
        mail.select("inbox")

        #Retrieve results for search of ALL.
        result, data = mail.search(None, "ALL")
        
        ids = data[0] # data is a list.
        id_list = ids.split() # ids is a space separated string
        latest_email_id = id_list[-1] # get the latest
        
        result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID

        # here's the body, which is raw text of the whole email.
        # NOTE: In Python3, make sure to decond the raw email like so.
        raw_email = data[0][1].decode('utf-8')

        email_message = email.message_from_string(raw_email)
    except Exception as e:
        error = True
        email_message = e
    
    #Since we are looking for a very specific sender - let's just check for said sender here.
    #if the email we got isn't from that address, then we'll ignore it.
    if email.utils.parseaddr(email_message['From'])[1] == "example2@example2.com":
        body = get_first_text_block(email_message)
        save_to_file(body)
    #if we did encounter an error, let's save that to the file here.
    elif error:
        save_to_file(email_message)
    else:
        save_to_file('An Unknown error occured, failed to fetch latest coding challenge.')


