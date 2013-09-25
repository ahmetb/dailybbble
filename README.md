# Dailybbble

This project crawls [Dribbble][dribbble] continuously to keep record of popular
designs and archive them by day. It also offers them over an API, RSS and 
daily newsletters.

## Introduction

The web interface runs at [dailybbble.herokuapp.com](http://dailybbble.herokuapp.com).
on Heroku platform.

Crawler runs as an executable Python daemon at file `fetcher.py`. It runs
continuously to retrieve data from Dribbble. You can use `supervisor` to
keep this process alive.

In addition you can send daily/weekly emails newsletters by scheduling
cronjobs (one runs every morning, one every Saturday noon) with commands

    python -m dailybbble.emailer daily
    python -m dailybbble.emailer weekly

## Installation

Windows Azure Table Storage is used as database. Therefore you need to 
initialize enviornment variables

* `AZURE_ACCOUNT_NAME`
* `AZURE_ACCOUNT_KEY`
* `AZURE_TABLEN_NAME` where shots are stored.

In addition, for e-mail subscription the following environment variables
are needed from [SendGrid][sendgrid] service:

* `SENDGRID_USERNAME`: account or API user name as in [https://sendgrid.com/credentials](https://sendgrid.com/credentials)
* `SENDGRID_PASSWORD`: account password or API key
* `SENDGRID_LIST_NAMES`: comma separated names of 2 recipient lists for daily
and weekly subscriptions (better you don't use commas while creating list
names)
* `SENDGRID_SENDER_NAME`: identity name of registered sender

For making use of `memcache` caching, configure the following
environment variables (auto-installed with Heroku Memcachier plugin):

* `MEMCACHIER_USERNAME`: SASL auth (if any)
* `MEMCACHIER_PASSWORD`: SASL auth (if any)
* `MEMCACHIER_SERVERS`: comma separated list of cache servers

You can use `$ heroku config:set KEY=VALUE` to persistently set environment
on Heroku app.


## License

Copyright 2013, Ahmet Alp Balkan

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

[dribbble]: http://dribbble.com
[sendgrid]: http://sendgrid.com
