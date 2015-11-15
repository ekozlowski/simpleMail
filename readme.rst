simpleMail
==========

I built simplemail because I was tired of having to specify so many options to
smtplib and email just to send myself a simple message!

Dependencies
============

NONE!  This should work out-of-the-box on a vanilla Python install.  It was tested
on Python 2.7.6 on a Mac OS X machine.

Usage
=====

You should look at simpleMail.py in the source, and set your options at the top there
accordingly.

If you are using Google, you will need to use a generated password, and your gmail
address as your username.  Here's a link to the place in Google to generate app
passwords:

https://security.google.com/settings/security/apppasswords

In the future, I may support a 'config.py', or other configruation options.  For now, 
this works for me. :)

If you have feedback or suggestions, please leave me a message!

ToDo
====

- Configuration seperate from the code.
- Better handling of starttls() if we don't need it.

Credits
=======

- Randy - My buddy at Alco for the inspiration.
- Pixabay - https://pixabay.com/en/lynx-bobcat-wildlife-predator-1019069/ where I got my AWESOME Lynx picture for my test attachment.

