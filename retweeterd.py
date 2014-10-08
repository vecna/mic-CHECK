#!/usr/bin/python


import time, sys
import base, pickle


class Retweeterd:

    def __init__(self, iname, rt_delay):

        self.iname = iname
        self.twinit = base.twitt(iname)
        self.rt_delay = rt_delay

    def loop(self):

        self.twinit.owner_init()

        favolist = self.twinit.api.GetFavorites()

        already_sent_id_cache = get_cache('singleuser')

        for sing_m in favolist:

            if sing_m.GetId() in already_sent_id_cache:
                continue

            already_sent_id_cache.append(sing_m.GetId())

            print "new message", sing_m.GetId(), sing_m.GetText()

            botcounter = 0
            failcounter = 0
            botlist = self.twinit.diskconf.get_botlist()
            for botfilename in botlist:

                print "short delay %d before %s" % (self.rt_delay, botfilename)
                time.sleep(self.rt_delay)

                # TODO probably can be optimized and used only self.twinit Obj
                bot = base.twitt(self.iname)
                bot.bot_init(botfilename, filename=True)

                try:
                    print "retweed per ", bot.authenticated, "id", sing_m.GetId()
                    # bot.api.PostRetweet(sing_m.GetId())
                except Exception as edata:
                    print "Fail! %s" % edata
                    failcounter += 1
                    self.twinit.diskconf.log("Fail RT: %d %s %s\n" % (failcounter, bot.authenticated, edata) )
                    continue

            botcounter += 1

            print "used %d users" % botcounter

        update_cache('singleuser', already_sent_id_cache)
        del already_sent_id_cache



def get_cache(username):

    fname = "/tmp/%s.cache" % username
    try:

        with file(fname) as f:
            already_sent_ids = pickle.load(f)
        assert isinstance(already_sent_ids, list), \
            "Invalid stuff retrivered from file %s (%s?)" % \
            (username, type(already_sent_ids))

    except Exception as e:

        print "Initialized dict in: %s" % fname
        already_sent_ids = list()

    return already_sent_ids

def update_cache(username, cacheblock):

    fname = "/tmp/%s.cache" % username
    try:
        with file(fname, 'w+') as f:
            pickle.dump(cacheblock, f)
    except Exception as e:
        print "Error pickle.dump: %s: %s" % (username, e)
        print cacheblock


def help(swname):

    print " %s INITIATIVE_NAME sleep_delay rt_delay" % swname
    print "\tsleep_delay: expressed in seconds, suggested 60-180"
    print "\trt_delay: expressed in seconds, suggested: 2-10"
    return 0


if __name__ == '__main__':

    if len(sys.argv) != 4:
        quit(help(sys.argv[0]))

    long_sleep = int(sys.argv[2])

    rt = Retweeterd(sys.argv[1], int(sys.argv[3]))

    print "You can interrupt this software only with ctrl+c"
    while True:
        rt.loop()
        print "Sleeping", long_sleep
        time.sleep(long_sleep)


