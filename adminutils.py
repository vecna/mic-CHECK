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
    base.Disku(initiative_name, create=True)

    return 0

def do_generate(iname):

    url, random_name = inner_do_generate(iname)
    print "url:", url
    print "random associated ID:", random_name
    return 0

def inner_do_generate(iname, supply_random=False):

    twiface = base.twitt(iname)

    if not supply_random:
        random_name= str(random.randint(1, 9999))
    else:
        random_name= str(supply_random)

    twiface.diskconf.log("Generating token for %s..." % random_name)

    url, oauth_token, oauth_secret = twiface.get_url_registration()

    # redunded: its the old logfile
    twiface.store_oauth_tmp_token(oauth_token, oauth_secret, random_name)

    tokens = { 'oauth_token': oauth_token , 'oauth_secret': oauth_secret }

    twiface.diskconf.log("... url %s TMP name associated %s" % (url, random_name) )

    twiface.diskconf.append_temporary(random_name, tokens)
    twiface.diskconf.log("Appended token in %s" % twiface.diskconf.tmptokenf)
    return url, random_name

def do_complete(iname, pin, urltoken):

    pincode = unicode(int(pin))
    random_token = unicode(int(urltoken))

    twiface = base.twitt(iname)

    tokens = twiface.diskconf.pop_temporary(random_token)
    username = twiface.complete_registration(pincode, tokens)
    # it print the username at the end

    if username:
        twiface.diskconf.log("username: %s registered!" % username)
    else:
        twiface.diskconf.log("do_complete fail with %s and %s" %
                             (pin, urltoken) )
    return username

def do_check(initiative_name):

    base.Disku(initiative_name, create=False)
    # TODO print some stuff - stats - etc

def help(swname):

    print " %s init | generate | complete <initiative_NAME>" % swname
    print "\tinit: initialize an application name"
    print "\tgenerate: generate a registration link"
    print "\tcomplete: +need the PIN as argument + Token from the URL"
    return 0

if __name__ == '__main__':

    if len(sys.argv) < 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help' or sys.argv[1] == 'help':
        quit(help(sys.argv[0]))

    if len(sys.argv) < 3:
        print "you've selected command: %s without specify the initiative name" % sys.argv[2]
        quit(help(sys.argv[0]))

    if len(sys.argv) != 3 or (sys.argv[2] == 'complete' and len(sys.argv) == 5):
        quit(help(sys.argv[0]))

    if sys.argv[1] == 'init':
        quit(do_init(sys.argv[2]))
    elif sys.argv[1] == 'generate':
        quit(do_generate(sys.argv[2]))
    elif sys.argv[1] == 'complete':
        quit(do_complete(sys.argv[2], sys.argv[3], sys.argv[4]))
    else:
        quit(help(sys.argv[0]))

