#! /usr/bin/python
# -*- coding: utf-8-*-

import json
import requests
import re
import datetime

# importing from virtual environment
import oauth_load
import models
import notify
import deactivate

# logging setup
import logging
logging.basicConfig(filename="DEBUG.log", level=logging.INFO)


# just for notification functionality, we could use read API token, but using
# oauth config for eventual asset deactivation POST request this script
# will make
get_creds = oauth_load.loadSecret()
account_id = get_creds["account_id"]
token = oauth_load.getAuthToken(get_creds)


# TAG BEING PULLED FROM BC CMS
tag = "BNP Paribas"


# ping Brightcove CMS with tag
def basic_search(token, tag, account_id):
    url = "https://cms.api.brightcove.com/v1/accounts/{}/videos?q=tags:{}".format(
        account_id, tag)
    print url
    headers = {"Authorization": "Bearer %s" % token}
    r = requests.get(url, headers=headers)
    res = json.loads(r.text)
    print(res)
    return res


BC_cms_response = basic_search(token, tag, account_id)

res_container = []
res_tupe = ()


# parse Brightcove CMS response and create tuple for each video asset that
# holds its video id, reference id created by Presto CMS import, and video
# name
def parse_res(BC_cms_response):
    for index, item in enumerate(BC_cms_response):
        id = item.get('id')
        reference_id = item.get('reference_id')
        title = item.get('name')
        res_tupe = (id, title, reference_id)
        res_container.append(res_tupe)
    # print res_container
    return res_container


parse_res_call = parse_res(BC_cms_response)


# checking if None in dic response, the None would be a lack of ref id.
# If no None values in tuple object res_container, then that tuple is added
# to presto_imports list
presto_imports = []


def ref_id_check(res_container):
    for item in res_container:
        print item
        if None in item:
            print "None type found in tuple, we're assuming None is the lack of ref id == no Presto import"
        else:
            presto_imports.append(item)
            for stuff in item:
                print(stuff)
    print(presto_imports)

ref_id_check(res_container)

Video = models.Video()

# parsing out tuples in presto_imports list
for tupes in presto_imports:
    # this is a Brightcove video id
    bc_id = tupes[0]
    #Video = models.Video()
    foo = models.session.query(models.Video).filter_by(video_id=bc_id).all()
    print(foo)

    # using implicit boolean-ness of empty list to check if list is empty
    # if not list is equivalent to checking if len(list) == 0, which makes a
    # list false
    if not foo:
        video = models.Video(video_id=tupes[0], name=tupes[1], ref_id=tupes[2])
        models.session.add(video)
        models.session.commit()

    # checking if video id from tupe in presto_imports already exists in the
    # db with instance.video_id
    else:
        for instance in foo:
            if bc_id == instance.video_id:
                print("This video", bc_id, "is already in the db")
                pass

            else:
                video = models.Video(
                    video_id=tupes[0],
                    name=tupes[1],
                    ref_id=tupes[2])
                models.session.add(video)
                models.session.commit()


# current time object
rightnow = datetime.datetime.utcnow()
diff = 0


def timer():
    ''' this establishes our timing for an asset based on the timestamp of its store to db and the current time. If it exceedes 23 hours, then we send email notification to adhere to publishing requirements '''

    for instance in models.session.query(
            models.Video).order_by(
            models.Video.id):
        print("\n")
        print(instance.name, instance.ref_id, instance.start_time)
        # after 24 hours, the diff will include '1 day' e.g. 1 day,
        # 8:48:17.928538

        # subtracting the current utcnow time from the time stamp for the asset
        # in the db
        diff = rightnow - instance.start_time
        print("UTCNOW time asset was stored in db: ")
        start_time = instance.start_time
        start_time = str(start_time)
        start_time = start_time.split()
        start_time = start_time[1]
        print(start_time)
        # print("\n")
        print("Time since Presto ingestion: ")
        print(diff)

        # probably an unnescessary try/except block but just on the off chance
        # that there's a glitch, and get_hour ends up with a '1 day' or more
        # string at index 0 (in the event that the time diff is more than 24
        # hours), we can catch that asset and also delete it from db and send
        # notification

        try:
            # break up items in string at each : and make into list
            get_hour = re.split(r":", str(diff))
            get_hour = int(get_hour[0])

            if get_hour == 0:

                # check off as expired in db
                # for every row in db, filter results by matching up id of video in db to id of video of current instance object in the outter for loop on line 126 via instance.id object.
                # then change the bool value from False to True via vid.expired
                # update
                for vid in models.session.query(
                        models.Video).filter_by(
                        id=instance.id):
                    vid.expired = True
                    models.session.commit()

                print("This video has expired: ")
                print(instance.name)

                if instance.alert_sent is not None:
                    pass
                else:
                    # send email notice
                    # contents of email message:
                    alert = "PLEASE UNPUBLISH: %s" % instance.name + \
                        " " + "BC ID: %s" % instance.video_id
                    # sending email
                    send_alert = notify.send_email(alert)
                    instance.alert_sent = alert
                    models.session.commit()
                    # deactivate expired asset in BC
                    bc_video_id = instance.video_id
                    deactivate.deactivate_request(bc_video_id)

            else:
                print("ok, asset was not given ref id over 24 hours ago yet...")
        except ValueError:
            get_hour = re.split(r":", str(diff))
            get_hour = get_hour[0]
            # separating the string from number separated by , at index 0 (e.g.
            # 'day 1, 20')
            get_hour = re.split(r",", get_hour)
            if isinstance(get_hour[0], str) == True and instance.alert_sent == None:
                print("WARNING: this asset has been given a refID over 24 hours ago (i.e. it has either 'Day 1' or older appended to the time diff string) and no alert was sent or exists in the db. Please check the db for this asset and make sure it is unpublished from your CMS")

timeit = timer()
