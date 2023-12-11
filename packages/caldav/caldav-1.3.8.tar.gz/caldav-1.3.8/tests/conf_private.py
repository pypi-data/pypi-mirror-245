from tests import compatibility_issues

## PRIVATE CALDAV SERVER(S) TO RUN TESTS TOWARDS
## Make a list of your own servers/accounts that you'd like to run the
## test towards.  Running the test suite towards a personal account
## should generally be safe, it should not mess up with content there
## and it should clean up after itself, but don't sue me if anything
## goes wrong ...

## Define your primary caldav server here
caldav_servers = [
    { # 0
        'url': "https://xandikos.tobixen.no/",
        "password": "kalenderfestøl",
        "username": "tobias",
        'incompatibilities': compatibility_issues.xandikos,
        'enable': True
    },
    { # 1
        'url': 'https://cloud.domainedessablons.fr/remote.php/dav/',
        'password': 'VeyshleewdmynJig7ob',
        'username': 'tobixen',
        'incompatibilities': compatibility_issues.nextcloud + ['unique_calendar_ids', 'non_existing_calendar_found', 'sticky_events'], ## the two latter seems to be a sticky calendar thing and/or impossible to create two calendars with the same name
        'enable': True # not working 100% as of 2022-04 ?
    },
    { # 2
        'url': 'https://ecloud.global/remote.php/dav/',
        'username': 'tobixen@e.email',
        'password': '/Test4Caldav.',
        'incompatibilities': compatibility_issues.nextcloud + ['unique_calendar_ids', 'non_existing_calendar_found'],
        'enable': True
    },
    { # 3
        ## <gregn@fastmail.com>
        'url': 'https://caldav.luckydrawcalendar.com/dav.php',
        'username': 'alpha',
        'password': 'passwordpassword',
        'incompatibilities': compatibility_issues.baikal + [ 'dav_not_supported' ],
        'enable': True ## getting only 401 after 2022-05-24, contacted greg at 2022-05-29
    },
    { # 4
        'url': 'https://zimbra.redpill-linpro.com/dav/',
        'username': 'tobias@redpill-linpro.com',
        'password': 'fiskesuppe kyllingsalat',
        'incompatibilities': compatibility_issues.zimbra,
        'enable': True
    },
    { # 5
        ## Does not get a proper response on get-current-principal propfind.
        ## should do more research into it, maybe
        'url': 'http://dav.cladmi.eu/cal.php',
        'principal_url': '/cal.php/principals/tbrox/',
        'username': 'tbrox',
        'password': 'testdigestauthenticationtbrox',
        'incompatibilities': [ 'no-current-user-principal' ], ## which is very strange, because from the web browser it does show this property
        'enable': False ## mkcalendar fails, calendar.events() fails ... but login works.  Should probably check more on this.  Hm.  It's some sabre thing, and it's possible to create new calendar through the web ui.  weird.
    },
    { # 6
        'url': 'http://calendar.tobixen.no:80/caldav.php/',
        'username': 'tobias',
        'password': '/family.',
        'enable': False, ## temporarily(?) down
        'incompatibilities': compatibility_issues.davical + [ 'no_freebusy_rfc4791' ]
    },

    ## It's needed with manual intervention to refresh accounts:
    { # 7
        'url': 'https://demo2.nextcloud.com/remote.php/dav/',
        'username': 'RQ6PbYE6KaNpfmHY',
        'password': 'demo2',
        'incompatibilities': compatibility_issues.nextcloud,
        'enable': False
    },
    { # 8
        'url': 'https://caldav.fastmail.com/dav/',
        'username': 'pythoncaldavtest@fastmail.com',
        'password': 'Q66M664VUQVJQ4ZJ',
        'incompatibilities': compatibility_issues.fastmail,
        'enable': False
    },
    { #9 - ref github issue #191 - swift.joy7282@fastmail.com
        'url': 'https://calendar.jeanes.us/caldav/',
        'username': 'tobixen',
        'password': 'skiing-chewer-tipping-sarcasm-knee',
        'incompatibilities': compatibility_issues.fastmail,
    },
    { #10 - https://calendar.robur.coop/ - ref https://github.com/python-caldav/caldav/issues/213
        'url': 'https://calendar.robur.coop/principals/',
        'username': 'caldavtest',
        'password': 'tycteucbok',
        'incompatibilities': compatibility_issues.robur
    },
    { #11 - reimer, telegram, issue 201 / 74196
        'url': 'https://dav.solox.de/p/Daniel.Reimer',
        'username': 'Daniel.Reimer',
        'password': 'solox',
        'enable': False,
        'incompatibilities': ['no_scheduling', "propfind_allprop_failure", "read_only"],
    },
    { #12 - my new davical server
        'url': 'https://davical.bekkenstenveien53c.oslo.no/caldav.php/',
        'username': 'testaccount1',
        'password': 'patriot-sunday-profane',
        'proxy': 'socks5://localhost:1080/', ## When on IPv4-only network
        'enable': True,
        'incompatibilities': [
            'fragile_sync_tokens', ## no issue raised yet.
            'fastmail_buggy_noexpand_date_search', ## https://gitlab.com/davical-project/davical/-/issues/280
            #'isnotdefined_not_working', ## https://gitlab.com/davical-project/davical/-/issues/281
            'vtodo_datesearch_nodtstart_task_is_skipped_in_closed_date_range',
        ]
    },
    { #13 - radicale (temp test)
        'url': 'http://localhost:5232/',
        'username': 'caldavtest',
        'password': 'dead beef family rock',
        'enable': False,
        'incompatibilities': ["no_default_calendar", "non_existing_calendar_found", "no_freebusy_rfc4791", 'no_scheduling', 'text_search_is_case_insensitive', 'text_search_is_exact_match_sometimes', 'combined_search_not_working', "calendar_order", "calendar_color"]
    },
    { #14 - SOGo
        'url': 'https://sogo.bekkenstenveien53c.oslo.no/SOGo/dav/',
        'username': 'test',
        'password': 'test',
        'incompatibilities': ["time_based_sync_tokens", "search_needs_comptype", "fastmail_buggy_noexpand_date_search", "text_search_not_working", "isnotdefined_not_working", 'no_journal', 'no_freebusy_rfc4791'] ## and in addition ... the requests are efficiently rate limited, as it spawns lots of postgresql connections all until a limit
    },
    { # 15 - posteo
        'url': 'https://posteo.de:8443/',
        'username': 'pycaltest',
        'password': 'stopped-prototype-frostingA1',
        'incompatibilities': ['no_scheduling', 'no_mkcalendar', 'no_journal', 'no_recurring_todo', 'no_sync_token'] ## no freebusy?
    },
    { # 16 - gmx
        'url': 'https://caldav.gmx.net/begenda/dav/users/pycaldavtest@gmx.net/',
        'username': 'pycaldavtest@gmx.net',
        'password': 'CalDavTest'
    }
]

if True:
    test_xandikos = True
    test_radicale = True
    caldav_servers = []
elif False:
    for x in caldav_servers:
        x['enable'] = False
    caldav_servers[16]['enable']=True

    test_xandikos = False
    test_radicale = False
else:
    caldav_servers = caldav_servers[9:10]
    #caldav_servers = []
    test_xandikos = True
    test_radicale = True


rfc6638_users = []
#for user in ('alpha', 'bravo', 'delta'):
#    rfc6638_users.append({'url': 'https://caldav.luckydrawcalendar.com/dav.php', 'username': user, 'password': 'passwordpassword'})

## SOGo virtual test server
## I did roughly those steps to set up a SOGo test server:
## 1) I download the ZEG - "Zero Effort Groupware" - from https://sourceforge.net/projects/sogo-zeg/
## 2) I installed virtualbox on my laptop
## 3) "virtualbox ~/Downloads/ZEG-5.0.0.ova" (TODO: probably it's possible to launch it "headless"?)
## 4) I clicked on some buttons to get the file "imported" and started
## 5) I went to "tools" -> "preferences" -> "network" and created a NatNetwork
## 6) I think I went to ZEG -> Settings -> Network and chose "Host-only Adapter"
## 7) SOGo was then available at http://192.168.56.101/ from my laptop
## 8) I added the lines below to my conf_private.py
#caldav_servers.append({
#    'url': 'http://192.168.56.101/SOGo/dav/',
#    'username': 'sogo1'.
#    'password': 'sogo'
#})
#for i in (1, 2, 3):
#    sogo = caldav_servers[-1].copy()
#    sogo['username'] = 'sogo%i' % i
#    rfc6638_users.append(sogo)

## MASTER SWITCHES FOR TEST SERVER SETUP
## With those configuration switches, pre-configured test servers in conf.py
## can be turned on or off

## test_public_test_servers - Use the list of common public test
## servers from conf.py.  As of 2020-10 no public test servers exists, so this option
## is currently moot :-(
test_public_test_servers = False

## test_private_test_servers - test using the list configured above in this file.
test_private_test_servers = True

## For usage by ../examples/scheduling_examples.py.  Should typically
## be three different users on the same caldav server.
#rfc6638_users = [ caldav_servers[0], caldav_servers[1], caldav_servers[2] ]
