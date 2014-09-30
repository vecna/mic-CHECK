#!/usr/bin/python
#
# This utility cover two needs of the admin:
#
# 1) generate authentication URL
# 2) submit PIN to complete registration


import base
import sys
import random


def do_init(initiative_name):

    print "Initializing: %s" % initiative_name
    # this at least go interactive and return a message/error
    base.Disku(initiative_name)

    return 0

def do_generate(iname):

    twiface = base.twitt(iname)

    random_name= str(random.randint(1, 9999))
    twiface.diskconf.log("Generating token for %s..." % random_name)

    url, oauth_token, oauth_secret = twiface.get_url_registration()

    # redunded: its the old logfile
    twiface.store_oauth_tmp_token(oauth_token, oauth_secret, random_name)

    tokens = { 'oauth_token': oauth_token , 'oauth_secret': oauth_secret }

    twiface.diskconf.log("... url %s TMP name associated %s" % (url, random_name) )

    twiface.diskconf.append_temporary(random_name, tokens)
    twiface.diskconf.log("Appended token in %s" % twiface.diskconf.tmptokenf)
    print url
    print random_name
    return 0

def do_complete(iname, pin, urltoken):

    pincode = int(pin)

    twiface = base.twitt(iname)

    tokens = twiface.diskconf.pop_temporary(urltoken)
    username = twiface.complete_registration(pincode, tokens)
    # it print the username at the end

    if username:
        twiface.diskconf.log("username: %s registered!" % username)
    else:
        twiface.diskconf.log("do_complete fail with %s and %s" %
                             (pin, urltoken) )
    return 0



def help(swname):

    print " %s init | generate | complete <initiative_NAME>" % swname
    print "\tinit: initialize an application name"
    print "\tgenerate: generate a registration link"
    print "\tcomplete: +need the PIN as argument + Token from the URL"
    return 0

if __name__ == '__main__':

    if len(sys.argv) != 3 and (sys.argv[2] == 'complete' and len(sys.argv) == 5):
        quit(help(sys.argv[0]))

    if sys.argv[1] == 'init':
        quit(do_init(sys.argv[2]))
    elif sys.argv[1] == 'generate':
        quit(do_generate(sys.argv[2]))
    elif sys.argv[1] == 'complete':
        quit(do_complete(sys.argv[2], sys.argv[3], sys.argv[4]))
    else:
        quit(help(sys.argv[0]))

