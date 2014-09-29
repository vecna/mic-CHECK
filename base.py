import os
import random
import json
import oauth2
import urlparse
import twitter
import sys


REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL  = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL        = 'https://api.twitter.com/oauth/authenticate'


DEFAULTDIR=".miccheck"
# DEFAULTINDEX="index.txt"

class Disku:


    def interactive_creation(self, iname):

        try:
            os.makedirs(self.init_dir)
        except OSError:
            pass

        if not os.access(self.ownerfname, os.W_OK):
            raise OSError("Can't access in write: %s" % self.ownerfname)

        print "Copy/Paste the Consumer Key (API Key): ",
        consumer_key = sys.stdin.readline()[:-1]
        print "Copy/Paste the Consumer Secret (API Secret): ",
        consumer_secret = sys.stdin.readline()[:-1]
        print "Copy/Paste the app name: ",
        app_name = sys.stdin.readline()[:-1]
        print "Copy/Paste the developer "



        self.apptokens = json.load(file(self.ownerfname, 'r'))

        for x in ['developer_secret_token', 'app_name', 'consumer_secret',
                  'consumer_key', 'developer_access_token', 'developer_username']:
            if not self.apptokens.has_key(x):
                em = "in owner_static is missing key %s" % x
                print em
                raise Exception(em)

    def __init__(self, initiative_name):

        self.loaded_initiative = initiative_name
        self.setup_environment_files()
        self.init_dir = os.path.join(self.micdir, initiative_name)
        self.ownerfname = os.path.join(self.init_dir, 'owner_static')

        if os.path.isdir(self.init_dir):
            print "Loaded initiative", initiative_name, "from", self.init_dir
        else:
            print "Creating initiative", initiative_name
            self.interactive_creation(initiative_name)

        self.log_file = os.path.join(self.init_dir, 'cache_info.log')


    def setup_environment_files(self):
        homedir = os.getenv('HOME')
        self.micdir = os.path.join(homedir, DEFAULTDIR)

    def log(self, a_string):
        x= file(self.log_file, 'w+')
        x.write(str(a_string))
        x.close()

    def get_botlist(self, appname):

        dirname, ownerfname = self.validate_appdir()

        stuff = os.listdir(dirname)

        botlist = []
        for single_f in stuff:
            if single_f.startswith('user_'):
                botlist.append(single_f)

        return botlist

    def validate_appdir(self):

        tmp_dirname = "%s_name" % self.micdir
        tmp_ownerfname = '%s/owner_static' % tmp_dirname

        if not os.path.isfile(tmp_ownerfname):
            em = "do not exists %s" % tmp_ownerfname
            print em
            raise Exception(em)


class twitt(object):

    def __init__(self, appname):

        self.diskconf = Disku(appname)

        self.ownerfname = os.path.join(self.diskconf.init_dir, 'owner_static')

        self.apptokens = json.load(file(self.ownerfname, 'r'))

        for x in ['developer_secret_token', 'app_name', 'consumer_secret',
                  'consumer_key', 'developer_access_token', 'developer_username']:
            if not self.apptokens.has_key(x):
                em = "in owner_static is missing key %s" % x
                print em
                raise Exception(em)

        self.appname = appname
        self.authenticated = None

    def owner_init(self):
        """
        This method is used only when you want act with App owner user
        """
        self.api = twitter.Api(self.apptokens['consumer_key'],
                               self.apptokens['consumer_secret'],
                               self.apptokens['developer_access_token'],
                               self.apptokens['developer_secret_token'])

        self.authenticated = self.apptokens['developer_username']


    def bot_init(self, botname, filename=False):
        """
        Bot is the supporter. just it's acting like a robot, so is not intended to be
        rude :P
        """

        if not filename:
            botfname = os.path.join(self.diskconf.micdir, "user_%s" % botname)
        else:
            botfname = botname

        if not os.path.isfile(botfname):
            # test to join dir
            botfname = os.path.join(self.diskconf.micdir, botfname)
            if not os.path.isfile(botfname):
                print "Not exist really the file %s - return" % botfname
                return

        print "Using bot: %s successful" % botfname

        self.usertokens = json.load(file(botfname, 'r'))

        for x in [ 'bot_secret_token', 'bot_access_token' ]:
            if not self.usertokens.has_key(x):
                em = "in %s is missing key %s" % (botfname, x)
                print em
                raise Exception(em)

        self.api = twitter.Api(self.apptokens['consumer_key'],
                               self.apptokens['consumer_secret'],
                               self.usertokens['bot_access_token'],
                               self.usertokens['bot_secret_token'])

        self.authenticated = botname

    def complete_registration(self, pin, tokens):
        """
        validate pin,
        obtain tokens,
        use tokens,
        get username,
        save the bot-ID-file
        """
        token_computed = oauth2.Token(tokens['oauth_token'], tokens['oauth_secret'])
        token_computed.set_verifier(pin)

        # rebuild oauth_consumer
        oauth_consumer = oauth2.Consumer(key=self.apptokens['consumer_key'],
                                         secret=self.apptokens['consumer_secret'])

        oauth_client  = oauth2.Client(oauth_consumer, token_computed)
        resp, content = oauth_client.request(ACCESS_TOKEN_URL,
                                             method='POST',
                                             body='oauth_callback=oob&oauth_verifier=%s' % pin)

        access_token  = dict(urlparse.parse_qsl(content))

        if resp['status'] != '200':
            print 'The request for a Token did not succeed: %s' % resp['status']
            raise Exception(resp)

        # creating the token object that would be eventually saved
        self.usertokens = {'bot_access_token' : access_token['oauth_token'],
                           'bot_secret_token' : access_token['oauth_token_secret']}

        self.api = twitter.Api(self.apptokens['consumer_key'],
                               self.apptokens['consumer_secret'],
                               self.usertokens['bot_access_token'],
                               self.usertokens['bot_secret_token'])

        try:
            credentials = self.api.VerifyCredentials()

        except Exception as edata:
            print "Error!", edata
            raise edata

        username = credentials.screen_name
        print username

        botfname = os.path.join(self.diskconf.micdir, "user_%s" % credentials.screen_name)

        try:
            self.diskconf.log("usertokens: %s %s\n" % (botfname, str(self.usertokens )) )
            f = file(botfname, 'w+')
            json.dump(self.usertokens, f)
        except Exception as edata:
            print "Error json dump %s %s" % (botfname, edata)
            raise edata

        return username


    def get_url_registration(self):

        # signature_method_hmac_sha1 = oauth2.SignatureMethod_HMAC_SHA1()
        # oauth2.SignatureMethod_HMAC_SHA1() # boh ?
        oauth_consumer = oauth2.Consumer(key=self.apptokens['consumer_key'],
                                         secret=self.apptokens['consumer_secret'])
        oauth_client = oauth2.Client(oauth_consumer)

        resp, content = oauth_client.request(REQUEST_TOKEN_URL, 'GET')

        if resp['status'] != '200':
            print "Invalid status", resp
            raise Exception("Invalid status %s" % resp['status'])

        request_token = dict(urlparse.parse_qsl(content))

        url = '%s?oauth_token=%s' % (AUTHORIZATION_URL, request_token['oauth_token'])
        return url, request_token['oauth_token'], request_token['oauth_token_secret']

    def store_oauth_tmp_token(self, oauth_token, oauth_secret, hexname):

        tokenfname = os.path.join(self.diskconf.micdir, "token_%s" % hexname)
        tokens = { 'oauth_token': oauth_token , 'oauth_secret': oauth_secret }
        json.dump(tokens, file(tokenfname, 'w+'))

    def get_oauth_tmp_token(self, hexname):

        try:
            tokenfname = os.path.join(self.diskconf.micdir,
                                      "token_%s" % hexname)
        except Exception as edata:
            print "Invalid format of partial token: [%s]: %s" % (hexname, edata)
            return None

        try:
            tokens = json.load(file(tokenfname))
            # os.unlink(tokenfname)
            return tokens
        except Exception as edata:
            print "Error in json load %s: %s" % (tokenfname, edata)
            return None

    def collect_followers(self):
        assert self.authenticated

        followers_obj = self.api.GetFollowers()
        self.followers = {}
        i = 0
        for single_follow in followers_obj:
            i += 1
            print "%d) [%s] =  %s with %d followers" % \
                  ( i, single_follow.GetId(), single_follow.screen_name, single_follow.followers_count )
            self.followers[single_follow.GetId()] = [ single_follow.screen_name, single_follow.followers_count ]
        print "readed %d followers" % i


    def frienzied(self, user):
        assert self.authenticated
        try:
            self.friend = self.api.CreateFriendship(user)
            print "[+] Added friend ", self.friend
        except Exception as excep:
            print "Unable to befriend %s: %s" % (user, excep)


    def list_f(self):
        assert self.authenticated
        self.Ifollow = self.api.GetFriends()
        print [u.screen_name for u in self.Ifollow]
        self.friends = {}
        for uu in self.Ifollow:
            self.friends[uu.GetId()] = uu.screen_name
            print "you follow %s : %s" % (uu.GetId(), uu.screen_name)

    def follow_someone(self, id):
        assert self.authenticated
        print self.api.CreateFriendship(id)
        print "Now I'm friend with", id

    def list_fid(self):
        assert self.authenticated
        FL = self.api.GetFriendIDs()
        print "friends ids", FL

    def direct_message(self, target, text):
        assert self.authenticated
        ret = self.api.PostDirectMessage(target, text)
        print ret

    def _random_string(self):
        return "Az %d-%d -mn- %d-%d Za" %\
               (random.randint(1, 90000), random.randint(1, 90000),
                random.randint(1, 90000), random.randint(1, 90000) )

    def spam(self, message):
        assert self.authenticated
        print self.api.VerifyCredentials().GetName(),
        print " ", message
        self.outputs.append( self.api.PostUpdate(message) )




