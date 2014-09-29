# mic-CHECK

If your hearing someone trustworthy, it's fine repeat and support the message spread.

## So, What ?

  * This application is a [twitter application](https://dev.twitter.com/rest/public) that basically recognize:
    * one or more Twitter user operating as "master".
    * one or more Twitter user operating as "supporter".

In order to be a supporter, the Twitter app need to be properly registered via *dev.twitter.com*

When one of the master account favorite a tweet, all the support retweet them. stop.

Is not a violation of Twitter policies, is not a violation of User Term of Service and Agreement and what you can have in mind. just, that.

## How does it work

**It's a working prototype**, not a stable industrial software. but this is the sequence:

### 1st step: create

[Login with your twitter account, and register an app](https://apps.twitter.com/), the account used here MAY have not relationship in the master/supporter.
Read the [Twitter rules about automation](https://support.twitter.com/articles/76915) because we want avoid make spam.

### 2nd step: permission

Assign to your app the permission (permission who is gonna to ask to the user) in "Read/Write", like here, (my app is called mic-check, your need to have a differet name because these name are unique):

![permission-twitterapp](https://cloud.githubusercontent.com/assets/89555/4451022/aa3eced8-482d-11e4-8ab1-cf059756cff1.png)


### 3rd step: keys

Go in keys, click in "Your Access Token" button to create your own access token. you'll need to make tests at least.

Now, you've to copy this keys in the script files.


