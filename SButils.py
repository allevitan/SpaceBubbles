#login/logout utils for SpaceBubbles

import random
import string
import hashlib
import re
import urllib

def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(username)

def valid_password(password):
    PASSWORD_RE = re.compile(r"^.{3,20}$")
    return PASSWORD_RE.match(password)

def valid_verify(password, verify):
    if password == verify:
        return True
    else:
        return None

def valid_email(email):
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
    return EMAIL_RE.match(email)


def obtain_gravatar(email):
    # using gravatar's example API code for python
    # le variables
    email = str(email)
    default=""
    size = 100

    # construct the url
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
    return gravatar_url



def make_salt(length=5):
    letters = string.ascii_letters
    salt = '' 
    for i in range(length):
        salt += random.choice(letters)
    return salt

def make_pw_hash(pw, salt=None):
    #Returns a string of the format "sha246 str of pw+salt | saltstr"
    if not salt: 
        salt = make_salt()
    return "%s|%s" % (hashlib.sha256(pw+salt).hexdigest(), salt)

def valid_pw(inputpw, h):
    salt = h.split('|')[1]
    if h == make_pw_hash(inputpw, salt):
        return True
    else:
        return None

# test= make_pw_hash('meep')
# print test
# print len(test)
# print valid_pw('meep', test)

# if SButils.valid_pw(login_input_pw, hashed_pw):
#     login the person ; it was correct
#     redirect as necessary