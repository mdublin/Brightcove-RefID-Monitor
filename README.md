
Setup as cron job on CentOS:

(Example to send log via email)
        
        */30 * * * * /home/local/username/Brightcove-refID-Monitor/main.py | tee /home/local/username/Brightcove-refID-Monitor/CronLogDirectory/RefID`date +\%Y-\%m-\%d-\%H:\%M:\%S`-cron.log | mailx -s "Email Subject Header" recipient@recipientemail.com



For sending emails from localhost (tested on Yosimite Mac OSX 10.10.5):

Step 1. Edit Postfix config file:

`$ sudo vim /etc/postfix/main.cf`

Make sure it's configured correctly by confirming follows lines are in your main.cf file:

`mydomain_fallback = localhost`

`mail_owner = _postfix`

`setgid_group = _postdrop`


Add these lines to the very end of main.cf file (here we're configuring for Gmail):

`#Gmail SMTP`

`relayhost=smtp.gmail.com:587`

`# Enable SASL authentication in the Postfix SMTP client.`

`smtp_sasl_auth_enable=yes`

`smtp_sasl_password_maps=hash:/etc/postfix/sasl_passwd`

`smtp_sasl_security_options=noanonymous`

`smtp_sasl_mechanism_filter=plain`

`# Enable Transport Layer Security (TLS), i.e. SSL.`

`smtp_use_tls=yes`

`smtp_tls_security_level=encrypt`

`tls_random_source=dev:/dev/urandom`

What does the above do? Here we're telling Postfix to use a GMAIL SMTP
server with Simple Authentication and Security Layer (SASL). Which will
be stored in the path “/etc/postfix/sasl_passwd“. You can use any other
SMTP provider (Hotmail, Yahoo, ETC…). You only need to know the SMTP
host and port.


Step 2. Create the sasl_passwd file with the SMTP creds:

create password file:

`$ sudo vim /etc/postfix/sasl_passwd`

Add the following to the sasl_passwd file:

`smtp.gmail.com:587 your_email@gmail.com:your_password`

Create the Postfix lookup table from the sasl_passwd file:

`$ sudo postmap /etc/postfix/sasl_passwd`

This creates the file sasl_passwd.db


Step 3. Restart Postfix to apply changes:

`$ sudo postfix reload`

If you get this error:

`$ postfix/postfix-script fatal the postfix mail system is not running`

Try:

`$ postfix start`

Then try the reload command again.


Step 4. Login into your Gmail account and switch the option for Access for less secure apps" or else you'll get a SASL authentication error.

Go to this URL:

`https://www.google.com/settings/security/lesssecureapps`


Step 5. Test it out:

`$ date | mail -s testing your_email@gmail.com`


Check the mail queue for any possible errors:

`$ mailq`

Checkout the postfix logs here:

`$ tail -f /var/log/mail.log`


If for some reason you need to clear the queue:

`$ sudo postsuper -d ALL`







