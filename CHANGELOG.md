# Change Log

## [Unreleased](https://github.com/omab/python-social-auth/tree/HEAD)

[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.3.0...HEAD)

## [v0.3.0](https://github.com/omab/python-social-auth/tree/v0.3.0) (2016-12-03)

Deprecated in favor of [python-social-auth organization](https://github.com/python-social-auth)

## [v0.2.21](https://github.com/omab/python-social-auth/tree/v0.2.21) (2016-08-15)

**Closed issues:**

- Django Migrations Broken [\#991](https://github.com/omab/python-social-auth/issues/991)

**Merged pull requests:**

- Fixed Django Migrations [\#993](https://github.com/omab/python-social-auth/pull/993) ([clintonb](https://github.com/clintonb))
- Rewrited pipeline.rst [\#992](https://github.com/omab/python-social-auth/pull/992) ([an0o0nym](https://github.com/an0o0nym))
- fix typo "Piepeline" -\> "Pipeline" [\#990](https://github.com/omab/python-social-auth/pull/990) ([das-g](https://github.com/das-g))
- Fixed Django \< 1.8 broken compatibility [\#986](https://github.com/omab/python-social-auth/pull/986) ([seroy](https://github.com/seroy))

## [v0.2.20](https://github.com/omab/python-social-auth/tree/v0.2.20) (2016-08-12)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.19...v0.2.20)

**Closed issues:**

- On production /complete/facebook just times out with a Gateway Timeout [\#972](https://github.com/omab/python-social-auth/issues/972)
- Support namespace via : [\#971](https://github.com/omab/python-social-auth/issues/971)
- Django Association model missing index [\#967](https://github.com/omab/python-social-auth/issues/967)
- VK auth using access token failed. Unable to retrieve email address. [\#943](https://github.com/omab/python-social-auth/issues/943)
- ImportError: No module named django\_app  [\#935](https://github.com/omab/python-social-auth/issues/935)
- ImportError: No module named 'example.local\_settings' with pyramid\_example [\#919](https://github.com/omab/python-social-auth/issues/919)
- "'User' object is not callable." issue. [\#895](https://github.com/omab/python-social-auth/issues/895)
- Support for the peewee ORM in storage. [\#877](https://github.com/omab/python-social-auth/issues/877)
- Meetup.com OAuth2 [\#677](https://github.com/omab/python-social-auth/issues/677)

**Merged pull requests:**

- fix comment word [\#983](https://github.com/omab/python-social-auth/pull/983) ([alexpantyukhin](https://github.com/alexpantyukhin))
- Added exception handling for user creation race condition in Django [\#975](https://github.com/omab/python-social-auth/pull/975) ([carsongee](https://github.com/carsongee))
- Update facebook api version to v2.7 [\#973](https://github.com/omab/python-social-auth/pull/973) ([c-bata](https://github.com/c-bata))
- Added index to Django Association model [\#969](https://github.com/omab/python-social-auth/pull/969) ([clintonb](https://github.com/clintonb))
- Corrected migration dependency [\#968](https://github.com/omab/python-social-auth/pull/968) ([clintonb](https://github.com/clintonb))
- Removed dep method get\_all\_field\_names method from Django 1.8+ [\#966](https://github.com/omab/python-social-auth/pull/966) ([zsiddique](https://github.com/zsiddique))
- Multiple hosts in redirect sanitaion. [\#965](https://github.com/omab/python-social-auth/pull/965) ([moorchegue](https://github.com/moorchegue))
- "else" scenario in Pyramid html func was causing an exception every time. [\#964](https://github.com/omab/python-social-auth/pull/964) ([moorchegue](https://github.com/moorchegue))
- Allow POST requests for auth method so OpenID forms could use it that way [\#963](https://github.com/omab/python-social-auth/pull/963) ([moorchegue](https://github.com/moorchegue))
- Add redirect\_uri to yammer docs [\#960](https://github.com/omab/python-social-auth/pull/960) ([m3brown](https://github.com/m3brown))
- Fix for flask/SQLAlchemy: commit on save \(but not when using Pyramid\) [\#957](https://github.com/omab/python-social-auth/pull/957) ([aoghina](https://github.com/aoghina))
- Switch from flask.ext.login to flask\_login [\#951](https://github.com/omab/python-social-auth/pull/951) ([EdwardBetts](https://github.com/EdwardBetts))
- username max\_length can be None [\#950](https://github.com/omab/python-social-auth/pull/950) ([EdwardBetts](https://github.com/EdwardBetts))
- Upgrade facebook backend api to latest version \(v2.6\) [\#941](https://github.com/omab/python-social-auth/pull/941) ([stphivos](https://github.com/stphivos))
- Line support added [\#937](https://github.com/omab/python-social-auth/pull/937) ([polyn0m](https://github.com/polyn0m))
- django migration should respect SOCIAL\_AUTH\_USER\_MODEL setting [\#936](https://github.com/omab/python-social-auth/pull/936) ([max-arnold](https://github.com/max-arnold))
- fix first and last name recovery [\#934](https://github.com/omab/python-social-auth/pull/934) ([PhilipGarnero](https://github.com/PhilipGarnero))
- fixes empty uid in coursera backend [\#933](https://github.com/omab/python-social-auth/pull/933) ([CrowbarKZ](https://github.com/CrowbarKZ))
- add support peewee for flask \#877 [\#932](https://github.com/omab/python-social-auth/pull/932) ([alexpantyukhin](https://github.com/alexpantyukhin))
- Fixed typo [\#928](https://github.com/omab/python-social-auth/pull/928) ([arogachev](https://github.com/arogachev))
- Fix mixed-content error of loading http over https scheme after disconnection from social account [\#924](https://github.com/omab/python-social-auth/pull/924) ([andela-kerinoso](https://github.com/andela-kerinoso))
- Add back-end for Edmodo [\#921](https://github.com/omab/python-social-auth/pull/921) ([browniebroke](https://github.com/browniebroke))
- Add Django AppConfig Label of "social\_auth" for migrations [\#916](https://github.com/omab/python-social-auth/pull/916) ([cclay](https://github.com/cclay))
- Update vk.rst [\#907](https://github.com/omab/python-social-auth/pull/907) ([slushkovsky](https://github.com/slushkovsky))
- VULNERABILITY - BaseStrategy.validate\_email\(\) doesn't actually check email address [\#900](https://github.com/omab/python-social-auth/pull/900) ([scottp-dpaw](https://github.com/scottp-dpaw))
- Removed broken link in use cases docs fixing \#860 [\#886](https://github.com/omab/python-social-auth/pull/886) ([RobinStephenson](https://github.com/RobinStephenson))
- Fixes bug where partial pipelines from abandoned login attempts will be resumed … [\#882](https://github.com/omab/python-social-auth/pull/882) ([SeanHayes](https://github.com/SeanHayes))
- Revise battlenet endpoint to return account ID and battletag [\#799](https://github.com/omab/python-social-auth/pull/799) ([ckcollab](https://github.com/ckcollab))
- Fixed 401 client redirect error for reddit backend [\#772](https://github.com/omab/python-social-auth/pull/772) ([opaqe](https://github.com/opaqe))

## [v0.2.19](https://github.com/omab/python-social-auth/tree/v0.2.19) (2016-04-29)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.18...v0.2.19)

**Closed issues:**

- \[Flask\] Not Logged in After Redirect [\#913](https://github.com/omab/python-social-auth/issues/913)
- Django: type\(social\_user.extra\_data\) == unicode [\#898](https://github.com/omab/python-social-auth/issues/898)
- Email is empty in login with Facebook [\#889](https://github.com/omab/python-social-auth/issues/889)

**Merged pull requests:**

- Storing token\_type in extra\_data field when using OAuth 2.0 [\#912](https://github.com/omab/python-social-auth/pull/912) ([clintonb](https://github.com/clintonb))
- Updates to OpenIdConnectAuth [\#911](https://github.com/omab/python-social-auth/pull/911) ([clintonb](https://github.com/clintonb))
- Corrected default value of JSONField [\#908](https://github.com/omab/python-social-auth/pull/908) ([clintonb](https://github.com/clintonb))

## [v0.2.18](https://github.com/omab/python-social-auth/tree/v0.2.18) (2016-04-20)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.17...v0.2.18)

## [v0.2.17](https://github.com/omab/python-social-auth/tree/v0.2.17) (2016-04-20)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.16...v0.2.17)

**Merged pull requests:**

- ADDED: upwork backend [\#904](https://github.com/omab/python-social-auth/pull/904) ([shepilov-vladislav](https://github.com/shepilov-vladislav))
- Add Sketchfab OAuth2 backend [\#901](https://github.com/omab/python-social-auth/pull/901) ([sylvinus](https://github.com/sylvinus))
- django 1.8+ compat to ensure to\_python is always called when accessing result from db.. [\#897](https://github.com/omab/python-social-auth/pull/897) ([sbussetti](https://github.com/sbussetti))

## [v0.2.16](https://github.com/omab/python-social-auth/tree/v0.2.16) (2016-04-13)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.15...v0.2.16)

## [v0.2.15](https://github.com/omab/python-social-auth/tree/v0.2.15) (2016-04-13)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.14...v0.2.15)

**Closed issues:**

- Warning with dependency six [\#885](https://github.com/omab/python-social-auth/issues/885)
- Password Reset Emails don't come if Authenticated via Python Social Auth [\#881](https://github.com/omab/python-social-auth/issues/881)
- I followed the documentation, but it didn't work for me. Would you please let me know where my PIPELINE is wrong? [\#867](https://github.com/omab/python-social-auth/issues/867)
- Is this AttributeError caused by facebook settings or python-social-auth? [\#865](https://github.com/omab/python-social-auth/issues/865)
- Google: Backend not found [\#862](https://github.com/omab/python-social-auth/issues/862)
- Django 1.9.2 ImportError: No module named 'social.apps.django\_app' [\#861](https://github.com/omab/python-social-auth/issues/861)
- Microsoft live oauth sign up/sign in issue [\#837](https://github.com/omab/python-social-auth/issues/837)
- Redirect url always ends with /\#\_=\_ [\#833](https://github.com/omab/python-social-auth/issues/833)
- Google Sign in problem [\#826](https://github.com/omab/python-social-auth/issues/826)
- Fitbit oauth2 [\#733](https://github.com/omab/python-social-auth/issues/733)

**Merged pull requests:**

- Add weixin public number oauth backend. [\#899](https://github.com/omab/python-social-auth/pull/899) ([duoduo369](https://github.com/duoduo369))
- Add support for Untappd as an OAuth v2 backend [\#894](https://github.com/omab/python-social-auth/pull/894) ([svvitale](https://github.com/svvitale))
- add coding oauth [\#892](https://github.com/omab/python-social-auth/pull/892) ([joway](https://github.com/joway))
- Add a backend for Classlink. [\#890](https://github.com/omab/python-social-auth/pull/890) ([antinescience](https://github.com/antinescience))
- Pass response to AuthCancel exception [\#883](https://github.com/omab/python-social-auth/pull/883) ([st4lk](https://github.com/st4lk))
- modifed wrong key names in pocket.py [\#878](https://github.com/omab/python-social-auth/pull/878) ([EunJung-Seo](https://github.com/EunJung-Seo))
- Fix typos [\#869](https://github.com/omab/python-social-auth/pull/869) ([Chronial](https://github.com/Chronial))
- Do not instantiate Logger directly [\#864](https://github.com/omab/python-social-auth/pull/864) ([browniebroke](https://github.com/browniebroke))
- Fix xgettext warning due to unknown encoding [\#856](https://github.com/omab/python-social-auth/pull/856) ([federicobond](https://github.com/federicobond))
- Update base.py [\#852](https://github.com/omab/python-social-auth/pull/852) ([hellvix](https://github.com/hellvix))
- Fix misspelled backend name [\#847](https://github.com/omab/python-social-auth/pull/847) ([victorgutemberg](https://github.com/victorgutemberg))
- Add some tests for Spotify backend + add a backend for Deezer music service [\#845](https://github.com/omab/python-social-auth/pull/845) ([khamaileon](https://github.com/khamaileon))
- \[Fix\] update odnoklasniki docs to new domain ok [\#836](https://github.com/omab/python-social-auth/pull/836) ([vanadium23](https://github.com/vanadium23))
- add github enterprise docs on how to specify the API URL [\#834](https://github.com/omab/python-social-auth/pull/834) ([iserko](https://github.com/iserko))
- Added optional 'include\_email' query param for Twitter backend. [\#829](https://github.com/omab/python-social-auth/pull/829) ([halfstrik](https://github.com/halfstrik))
- Fix ImportError: cannot import name ‘urlencode’ in Python3 [\#828](https://github.com/omab/python-social-auth/pull/828) ([mishbahr](https://github.com/mishbahr))
- Fix wrong evaluation of boolean kwargs [\#824](https://github.com/omab/python-social-auth/pull/824) ([falknes](https://github.com/falknes))
- SAML: raise AuthMissingParameter if idp param missing [\#821](https://github.com/omab/python-social-auth/pull/821) ([omarkhan](https://github.com/omarkhan))
- added support for ArcGIS OAuth2 [\#820](https://github.com/omab/python-social-auth/pull/820) ([aspcanada](https://github.com/aspcanada))
- BaseOAuth2: Store access token in response if it does not exist [\#816](https://github.com/omab/python-social-auth/pull/816) ([kchange](https://github.com/kchange))
- Minor backend fixes [\#815](https://github.com/omab/python-social-auth/pull/815) ([mback2k](https://github.com/mback2k))
- Fix Django 1.10 Deprecation Warning "SubfieldBase has been deprecated." [\#813](https://github.com/omab/python-social-auth/pull/813) ([contracode](https://github.com/contracode))
- Fix typo: "attacht he" -\> "attach the" [\#808](https://github.com/omab/python-social-auth/pull/808) ([smholloway](https://github.com/smholloway))
- Azure AD updates [\#807](https://github.com/omab/python-social-auth/pull/807) ([vinhub](https://github.com/vinhub))
- Remove unused response arg from user\_data method of yandex backend [\#784](https://github.com/omab/python-social-auth/pull/784) ([SrgyPetrov](https://github.com/SrgyPetrov))
- Support all kind of data type \(like uuid\) of User.id on Pyramid [\#769](https://github.com/omab/python-social-auth/pull/769) ([cjltsod](https://github.com/cjltsod))

## [v0.2.14](https://github.com/omab/python-social-auth/tree/v0.2.14) (2016-01-25)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.13...v0.2.14)

**Closed issues:**

- Error "imported before its application was loaded" [\#809](https://github.com/omab/python-social-auth/issues/809)
- Django 1.9.0 Deprecation Warning [\#804](https://github.com/omab/python-social-auth/issues/804)
- Migration error on update 0.2.6 -\> 0.2.7 [\#761](https://github.com/omab/python-social-auth/issues/761)
- Backends: user\_data vs extra\_data? [\#759](https://github.com/omab/python-social-auth/issues/759)
- example/django\_example twitter error [\#742](https://github.com/omab/python-social-auth/issues/742)
- Object of type map has no length [\#633](https://github.com/omab/python-social-auth/issues/633)

**Merged pull requests:**

- Add support for Drip Email Marketing Site [\#810](https://github.com/omab/python-social-auth/pull/810) ([buddylindsey](https://github.com/buddylindsey))
- Fix Django 1.10 deprecation warnings [\#806](https://github.com/omab/python-social-auth/pull/806) ([yprez](https://github.com/yprez))
- bugs in social\_user and associate\_by\_email return values [\#800](https://github.com/omab/python-social-auth/pull/800) ([falcon1kr](https://github.com/falcon1kr))
- Changed instagram backend to new authorization routes [\#797](https://github.com/omab/python-social-auth/pull/797) ([clybob](https://github.com/clybob))
- Update settings.rst [\#793](https://github.com/omab/python-social-auth/pull/793) ([skolsuper](https://github.com/skolsuper))
- Add naver.com OAuth2 backend [\#789](https://github.com/omab/python-social-auth/pull/789) ([se0kjun](https://github.com/se0kjun))
- Formatter fixes for SAML to support Py2.6 [\#783](https://github.com/omab/python-social-auth/pull/783) ([matburt](https://github.com/matburt))
- Add pinterest backend [\#774](https://github.com/omab/python-social-auth/pull/774) ([scailer](https://github.com/scailer))
- Fix typo [\#768](https://github.com/omab/python-social-auth/pull/768) ([mprunell](https://github.com/mprunell))
- Fixes a few grammar issues in the docs [\#764](https://github.com/omab/python-social-auth/pull/764) ([kevinharvey](https://github.com/kevinharvey))
- use qq openid as username [\#763](https://github.com/omab/python-social-auth/pull/763) ([lneoe](https://github.com/lneoe))
- Fix a few typos in backends [\#760](https://github.com/omab/python-social-auth/pull/760) ([pzrq](https://github.com/pzrq))
- Fix vk backend [\#757](https://github.com/omab/python-social-auth/pull/757) ([truetug](https://github.com/truetug))
- Fix odnoklassniki backend [\#756](https://github.com/omab/python-social-auth/pull/756) ([truetug](https://github.com/truetug))
- Store all tokens when tokens are refreshed [\#753](https://github.com/omab/python-social-auth/pull/753) ([mvschaik](https://github.com/mvschaik))
- Added support for NGPVAN ActionID OpenID [\#750](https://github.com/omab/python-social-auth/pull/750) ([nickcatal](https://github.com/nickcatal))
- Python 3 support for facebook-app backend [\#749](https://github.com/omab/python-social-auth/pull/749) ([jhmaddox](https://github.com/jhmaddox))
- Save extra\_data on login [\#748](https://github.com/omab/python-social-auth/pull/748) ([mvschaik](https://github.com/mvschaik))
- Update URLs to match new site and remove OAuth comment. [\#744](https://github.com/omab/python-social-auth/pull/744) ([lukos](https://github.com/lukos))
- Fitbit OAuth 2.0 support [\#743](https://github.com/omab/python-social-auth/pull/743) ([robbiet480](https://github.com/robbiet480))
- added AuthUnreachableProvider exception to documentation [\#729](https://github.com/omab/python-social-auth/pull/729) ([Qlio](https://github.com/Qlio))
- Add REDIRECT\_STATE = False [\#725](https://github.com/omab/python-social-auth/pull/725) ([webjunkie](https://github.com/webjunkie))
- Tuple in pipeline's documentation should be ended with coma [\#712](https://github.com/omab/python-social-auth/pull/712) ([JerzySpendel](https://github.com/JerzySpendel))
- Fix redirect\_uri issue with tornado reversed url [\#674](https://github.com/omab/python-social-auth/pull/674) ([mvschaik](https://github.com/mvschaik))

## [v0.2.13](https://github.com/omab/python-social-auth/tree/v0.2.13) (2015-09-25)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.12...v0.2.13)

**Closed issues:**

- Signup by OAuth access\_token example question [\#737](https://github.com/omab/python-social-auth/issues/737)
- Connecting to a "django oAuth toolkit" based oAuth provider [\#727](https://github.com/omab/python-social-auth/issues/727)
- Exception Value: 'module' object has no attribute 'FacebookOauth2' [\#722](https://github.com/omab/python-social-auth/issues/722)
- Google OAuth2 - stopped working, now getting JSONDecodeError for token response [\#718](https://github.com/omab/python-social-auth/issues/718)
- Is there a conflict with django-debug-toolbar? [\#714](https://github.com/omab/python-social-auth/issues/714)
- FORM\_HTML and Legacy Auth [\#705](https://github.com/omab/python-social-auth/issues/705)
-   Authentication process canceled with Spotify auth \(invalid\_client\) [\#703](https://github.com/omab/python-social-auth/issues/703)
- \[Question\] How to tell if a user was created or existing [\#701](https://github.com/omab/python-social-auth/issues/701)
- Make an abstract verstion of django's UserSocialAuth's model so it can be extended [\#698](https://github.com/omab/python-social-auth/issues/698)
- Problem porting from django-social-auth to python-social-auth [\#682](https://github.com/omab/python-social-auth/issues/682)
- django\_app/default: Migration 0003\_alter\_email\_max\_length wrong for Django 1.7 [\#622](https://github.com/omab/python-social-auth/issues/622)

**Merged pull requests:**

- VK API workflow fix if error happens on vk-side [\#736](https://github.com/omab/python-social-auth/pull/736) ([alrusdi](https://github.com/alrusdi))
- Added justgiving.com OAuth2 backend [\#728](https://github.com/omab/python-social-auth/pull/728) ([mwillmott](https://github.com/mwillmott))
- Fix typo in pipeline doc [\#720](https://github.com/omab/python-social-auth/pull/720) ([Andygmb](https://github.com/Andygmb))
- Update facebook.rst [\#717](https://github.com/omab/python-social-auth/pull/717) ([zergu](https://github.com/zergu))
- Support Pyramid Authentication Policies [\#710](https://github.com/omab/python-social-auth/pull/710) ([cjltsod](https://github.com/cjltsod))
- Fix typo [\#709](https://github.com/omab/python-social-auth/pull/709) ([ajoyoommen](https://github.com/ajoyoommen))
- Fix 'QueryDict' object has no attribute 'dicts' [\#707](https://github.com/omab/python-social-auth/pull/707) ([webjunkie](https://github.com/webjunkie))
- Add support for Uber OAuth2 - Uber API v1 [\#706](https://github.com/omab/python-social-auth/pull/706) ([henocdz](https://github.com/henocdz))
- Fix \#703 invalid\_client error with Spotify backend [\#704](https://github.com/omab/python-social-auth/pull/704) ([khamaileon](https://github.com/khamaileon))
- additional "how it fits together" documentation [\#700](https://github.com/omab/python-social-auth/pull/700) ([ccurvey](https://github.com/ccurvey))
- Make an abstract verstion of django's UserSocialAuth's model so it can be extended \(fixes \#698\) [\#699](https://github.com/omab/python-social-auth/pull/699) ([troygrosfield](https://github.com/troygrosfield))
- flask\_me\_example fix [\#696](https://github.com/omab/python-social-auth/pull/696) ([jameslittle](https://github.com/jameslittle))
- removed @app.teardown\_request since it is called before @app.teardown… [\#690](https://github.com/omab/python-social-auth/pull/690) ([asimcan](https://github.com/asimcan))
- Remove debug printing from BaseOAuth2 backend [\#689](https://github.com/omab/python-social-auth/pull/689) ([gcheshkov](https://github.com/gcheshkov))
- support for goclio.eu service [\#686](https://github.com/omab/python-social-auth/pull/686) ([jneves](https://github.com/jneves))
- text -\> content solves "is not JSON serializable" [\#685](https://github.com/omab/python-social-auth/pull/685) ([JordanReiter](https://github.com/JordanReiter))
- Close \#622 by explicitly setting email length \(compatibility with Django 1.7\) [\#684](https://github.com/omab/python-social-auth/pull/684) ([frankier](https://github.com/frankier))
- Add orbi backend [\#683](https://github.com/omab/python-social-auth/pull/683) ([jeyraof](https://github.com/jeyraof))
- Fix Clef backend [\#681](https://github.com/omab/python-social-auth/pull/681) ([jessepollak](https://github.com/jessepollak))
- Meetup.com OAuth2 provider [\#678](https://github.com/omab/python-social-auth/pull/678) ([bluszcz](https://github.com/bluszcz))
- echosign OAuth2 backend [\#676](https://github.com/omab/python-social-auth/pull/676) ([paxapy](https://github.com/paxapy))

## [v0.2.12](https://github.com/omab/python-social-auth/tree/v0.2.12) (2015-07-10)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.11...v0.2.12)

**Closed issues:**

- Pipeline `user\_details` not changing empty and protected user fields [\#671](https://github.com/omab/python-social-auth/issues/671)
- Instagram: Missing needed parameter state [\#643](https://github.com/omab/python-social-auth/issues/643)
- Could not find required distribution python-social-auth [\#638](https://github.com/omab/python-social-auth/issues/638)
- Installing python-social-auth as a dependecie for mailman3 with buildout fails [\#623](https://github.com/omab/python-social-auth/issues/623)

**Merged pull requests:**

- Improve docs on SOCIAL\_AUTH\_NEW\_USER\_REDIRECT\_URL [\#673](https://github.com/omab/python-social-auth/pull/673) ([eshellman](https://github.com/eshellman))
- PR fix `user\_details` pipeline issue [\#672](https://github.com/omab/python-social-auth/pull/672) ([maxsocl](https://github.com/maxsocl))
- Fix cookie handling for tornado [\#667](https://github.com/omab/python-social-auth/pull/667) ([mvschaik](https://github.com/mvschaik))
- added support for Github Enterprise [\#662](https://github.com/omab/python-social-auth/pull/662) ([iserko](https://github.com/iserko))
- Withings Backend [\#658](https://github.com/omab/python-social-auth/pull/658) ([tomasgarzon](https://github.com/tomasgarzon))
- Use official python-saml 2.1.3 release, remove now-unsupported setting [\#657](https://github.com/omab/python-social-auth/pull/657) ([bradenmacdonald](https://github.com/bradenmacdonald))
- Fix wrong placement of changelog commits in 76a27b2 [\#656](https://github.com/omab/python-social-auth/pull/656) ([bradenmacdonald](https://github.com/bradenmacdonald))
- Python3 fixes for Tornado [\#649](https://github.com/omab/python-social-auth/pull/649) ([mvschaik](https://github.com/mvschaik))
- Keep the egg-info directory in the sdist [\#635](https://github.com/omab/python-social-auth/pull/635) ([abompard](https://github.com/abompard))

## [v0.2.11](https://github.com/omab/python-social-auth/tree/v0.2.11) (2015-06-24)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.10...v0.2.11)

**Merged pull requests:**

- Added an OAuth2 backend for Bitbucket [\#653](https://github.com/omab/python-social-auth/pull/653) ([mark-adams](https://github.com/mark-adams))
- Updated Bitbucket backends to use newer v2.0 APIs [\#652](https://github.com/omab/python-social-auth/pull/652) ([mark-adams](https://github.com/mark-adams))
- SAML support [\#616](https://github.com/omab/python-social-auth/pull/616) ([bradenmacdonald](https://github.com/bradenmacdonald))

## [v0.2.10](https://github.com/omab/python-social-auth/tree/v0.2.10) (2015-05-30)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.9...v0.2.10)

**Closed issues:**

- "UserSocialAuth.user" must be a "MyUser" instance [\#631](https://github.com/omab/python-social-auth/issues/631)
- ImportError: No module named packages.urllib3.poolmanager [\#617](https://github.com/omab/python-social-auth/issues/617)
- AuthStateMissing: Session value state missing on web.py example integration [\#611](https://github.com/omab/python-social-auth/issues/611)
- return pipeline data when doing oauth association [\#610](https://github.com/omab/python-social-auth/issues/610)
- Reverse with trailing slash in django urls is broken since 0.2.4 to 0.2.7 [\#609](https://github.com/omab/python-social-auth/issues/609)

**Merged pull requests:**

- Resubmitting pull request to add Azure Active Directory support [\#632](https://github.com/omab/python-social-auth/pull/632) ([vinhub](https://github.com/vinhub))
- Fixes missing packages.urllib3.poolmanager \(fixes \#617\) [\#626](https://github.com/omab/python-social-auth/pull/626) ([marekjalovec](https://github.com/marekjalovec))
- fix Fitbit OAuth 1 authorization URL [\#625](https://github.com/omab/python-social-auth/pull/625) ([blurrcat](https://github.com/blurrcat))
- add weixin backends [\#621](https://github.com/omab/python-social-auth/pull/621) ([duoduo369](https://github.com/duoduo369))
- Add a DigitalOcean backend. [\#619](https://github.com/omab/python-social-auth/pull/619) ([andrewsomething](https://github.com/andrewsomething))

## [v0.2.9](https://github.com/omab/python-social-auth/tree/v0.2.9) (2015-05-07)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.8...v0.2.9)

## [v0.2.8](https://github.com/omab/python-social-auth/tree/v0.2.8) (2015-05-07)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.7...v0.2.8)

**Closed issues:**

- Can't get a Google OAuth2 refresh\_token [\#607](https://github.com/omab/python-social-auth/issues/607)
- Get the current logged user in the template [\#605](https://github.com/omab/python-social-auth/issues/605)
- Two diferent user profiles [\#604](https://github.com/omab/python-social-auth/issues/604)
- Login with Amazon TLS requests [\#603](https://github.com/omab/python-social-auth/issues/603)
- Release apps.py for apps [\#601](https://github.com/omab/python-social-auth/issues/601)
-  migrations [\#600](https://github.com/omab/python-social-auth/issues/600)
- Authentication failed: Can't connect to HTTPS URL because the SSL module is not available. [\#598](https://github.com/omab/python-social-auth/issues/598)
- ConnectionError at /complete/steam You have not defined a default connection [\#597](https://github.com/omab/python-social-auth/issues/597)
- uncompleted extra\_data for access\_token, code, and expires in Google+ [\#596](https://github.com/omab/python-social-auth/issues/596)
- Token error: Missing unauthorized token [\#589](https://github.com/omab/python-social-auth/issues/589)
- Email validation needs an email parameter \(docs\) [\#577](https://github.com/omab/python-social-auth/issues/577)
- Login pipeline trying to create new user when user exists [\#562](https://github.com/omab/python-social-auth/issues/562)

**Merged pull requests:**

- Just add Moves App to the list of providers on README  [\#606](https://github.com/omab/python-social-auth/pull/606) ([avibrazil](https://github.com/avibrazil))
- ChangeTip Backend [\#599](https://github.com/omab/python-social-auth/pull/599) ([gorillamania](https://github.com/gorillamania))

## [v0.2.7](https://github.com/omab/python-social-auth/tree/v0.2.7) (2015-04-19)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.6...v0.2.7)

**Closed issues:**

- CLEAN\_USERNAME\_REGEX  error [\#594](https://github.com/omab/python-social-auth/issues/594)
- JSONDecodeError at /complete/facebook [\#592](https://github.com/omab/python-social-auth/issues/592)

**Merged pull requests:**

- Fix the final\_username may be empty and will skip the loop. [\#595](https://github.com/omab/python-social-auth/pull/595) ([littlezz](https://github.com/littlezz))
- Alter email max length for Django app [\#593](https://github.com/omab/python-social-auth/pull/593) ([JonesChi](https://github.com/JonesChi))
- Append trailing slash in Django [\#591](https://github.com/omab/python-social-auth/pull/591) ([chripede](https://github.com/chripede))

## [v0.2.6](https://github.com/omab/python-social-auth/tree/v0.2.6) (2015-04-14)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.5...v0.2.6)

**Closed issues:**

- pypi package version 0.2.5 is missing requirements.txt from tests [\#590](https://github.com/omab/python-social-auth/issues/590)
- TypeError: object of type 'map' has no len\(\) [\#588](https://github.com/omab/python-social-auth/issues/588)
- please support weixin auth [\#481](https://github.com/omab/python-social-auth/issues/481)
-  How to take the user's address on facebook? This has already been implemented? [\#470](https://github.com/omab/python-social-auth/issues/470)
- django social auth get wrong access\_token from google oauth2 [\#467](https://github.com/omab/python-social-auth/issues/467)
- Reddit OAuth2 401 Client Error Unauthorized [\#440](https://github.com/omab/python-social-auth/issues/440)
- twitter login: 401 Client Error: Authorization Required [\#400](https://github.com/omab/python-social-auth/issues/400)
- remove incomplete partial pipeline data from session [\#325](https://github.com/omab/python-social-auth/issues/325)

## [v0.2.5](https://github.com/omab/python-social-auth/tree/v0.2.5) (2015-04-13)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.4...v0.2.5)

**Closed issues:**

- Setting user.is\_active to false at end of pipeline logs out user [\#586](https://github.com/omab/python-social-auth/issues/586)

## [v0.2.4](https://github.com/omab/python-social-auth/tree/v0.2.4) (2015-04-12)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.3...v0.2.4)

**Closed issues:**

- djangopackages.com still referes to the old project \(django-social-auth\) [\#585](https://github.com/omab/python-social-auth/issues/585)
- warnings in Django 1.8 [\#584](https://github.com/omab/python-social-auth/issues/584)
- Problems with upgrading Django Packages to python-social-auth [\#582](https://github.com/omab/python-social-auth/issues/582)
- Django 1.9 Warnings [\#581](https://github.com/omab/python-social-auth/issues/581)
- django 1.8, ImportError: No module named social\_auth.context\_processors [\#579](https://github.com/omab/python-social-auth/issues/579)
- sdist tarball is missing some files and dirs [\#578](https://github.com/omab/python-social-auth/issues/578)
- Using twitter backend with mongoengine [\#576](https://github.com/omab/python-social-auth/issues/576)
- Issues while using Custom User model [\#575](https://github.com/omab/python-social-auth/issues/575)
- Throw a more helpful exception when oauth\_consumer\_key is missing for OAuth1 [\#574](https://github.com/omab/python-social-auth/issues/574)
- sqlalchemy\_orm: ImportError: No module named transaction [\#572](https://github.com/omab/python-social-auth/issues/572)
- New version ? [\#571](https://github.com/omab/python-social-auth/issues/571)
- logout without disconnect [\#568](https://github.com/omab/python-social-auth/issues/568)
- SSL issue with google oauth2 [\#566](https://github.com/omab/python-social-auth/issues/566)
- next parameter containing get parameters [\#565](https://github.com/omab/python-social-auth/issues/565)
- get\(\) returned more than one UserSocialAuth -- it returned 2! [\#553](https://github.com/omab/python-social-auth/issues/553)
- RemovedInDjango19Warning [\#551](https://github.com/omab/python-social-auth/issues/551)
- Development/debug option to stub backend while developing [\#546](https://github.com/omab/python-social-auth/issues/546)
- weibo access\_token ajax auth fail [\#532](https://github.com/omab/python-social-auth/issues/532)
- Change PyJWT dependency version in setup.py from PyJWT==0.4.1 to PyJWT\>=0.4.1 [\#531](https://github.com/omab/python-social-auth/issues/531)
- Behance authentication  [\#530](https://github.com/omab/python-social-auth/issues/530)
- upstream sent too big header while reading response header from upstream [\#527](https://github.com/omab/python-social-auth/issues/527)
- Fails to work with Django 1.8 [\#526](https://github.com/omab/python-social-auth/issues/526)
- AttributeError in VKOAuth2 [\#525](https://github.com/omab/python-social-auth/issues/525)
- Login user with Email address instead of Username [\#513](https://github.com/omab/python-social-auth/issues/513)
- Actually Log Exceptions in SocialAuthExceptionMiddleware [\#507](https://github.com/omab/python-social-auth/issues/507)
- Don't require trailing slashes [\#505](https://github.com/omab/python-social-auth/issues/505)
- django example [\#504](https://github.com/omab/python-social-auth/issues/504)
- complete/mendeley-oauth2 not successful [\#501](https://github.com/omab/python-social-auth/issues/501)
- Unable to refresh google oauth2 token after update python social auth to 0.2.1 [\#485](https://github.com/omab/python-social-auth/issues/485)
- revoke\_token\_params &  revoke\_token\_headers are missing for GooglePlusAuth [\#484](https://github.com/omab/python-social-auth/issues/484)
- Microsoft Live Oauth2  Error [\#483](https://github.com/omab/python-social-auth/issues/483)
- Support Facebook Graph API 2.2 [\#480](https://github.com/omab/python-social-auth/issues/480)
- Spotify setting names are incorrect. [\#475](https://github.com/omab/python-social-auth/issues/475)
- Django adds migration [\#474](https://github.com/omab/python-social-auth/issues/474)
- SOCIAL\_AUTH\_LINKEDIN\_FIELD\_OAUTH2\_SELECTORS Not being used to populate user creation backend [\#466](https://github.com/omab/python-social-auth/issues/466)
- Yahoo OAuth 2? [\#463](https://github.com/omab/python-social-auth/issues/463)
- Docs for SOCIAL\_AUTH\_PROTECTED\_USER\_FIELDS misleading [\#459](https://github.com/omab/python-social-auth/issues/459)
- Gracefully handle AuthExceptions [\#458](https://github.com/omab/python-social-auth/issues/458)
- why context processor replace hyphen by underscore in google-oauth2 ? [\#457](https://github.com/omab/python-social-auth/issues/457)
- On linkedin,github login: AttributeError at http://llovebaimuda.herokuapp.com:8000/complete/github/ 'GithubBackend' object has no attribute 'auth\_allowed' [\#442](https://github.com/omab/python-social-auth/issues/442)
- GET /disconnect/\<backend\>/ HTTP/1.0" 405 [\#438](https://github.com/omab/python-social-auth/issues/438)
- Facebook api change  [\#424](https://github.com/omab/python-social-auth/issues/424)
- Import error: no module named google\_auth [\#423](https://github.com/omab/python-social-auth/issues/423)
- Django: Google+ disconnect does not actually disconnect [\#394](https://github.com/omab/python-social-auth/issues/394)
- How to save user to db without 'request' in register\_by\_access\_token\(request, backend\) function? [\#393](https://github.com/omab/python-social-auth/issues/393)
- Support Paste style configuration [\#392](https://github.com/omab/python-social-auth/issues/392)
- Google OAuth2 gives 400 error, FB 500 error [\#364](https://github.com/omab/python-social-auth/issues/364)
- Django - Google Authentication - Create Account [\#362](https://github.com/omab/python-social-auth/issues/362)
- Make Migrations Backward-Compatible with South [\#353](https://github.com/omab/python-social-auth/issues/353)
- Github access\_token never stored [\#344](https://github.com/omab/python-social-auth/issues/344)
- How to extends django orm mixins [\#343](https://github.com/omab/python-social-auth/issues/343)
- a few issues [\#333](https://github.com/omab/python-social-auth/issues/333)
- south migration for django app? [\#331](https://github.com/omab/python-social-auth/issues/331)
- Cannot log out from GooglePlus Auth. Homepage keeps calling its GooglePlus callback [\#316](https://github.com/omab/python-social-auth/issues/316)
- change log [\#313](https://github.com/omab/python-social-auth/issues/313)
- Return 503 instead of raise 500 error when auth provider not accessible [\#304](https://github.com/omab/python-social-auth/issues/304)
- Facebook SOCIAL\_AUTH\_FACEBOOK\_SCOPE not working as expected [\#294](https://github.com/omab/python-social-auth/issues/294)
- Add Django 1.7 migrations [\#270](https://github.com/omab/python-social-auth/issues/270)
- IntegrityError at /social/complete/facebook/ duplicate key value violates unique constraint "userprofile\_user\_email\_key" [\#208](https://github.com/omab/python-social-auth/issues/208)

**Merged pull requests:**

- Build a wheel, and upload with twine [\#583](https://github.com/omab/python-social-auth/pull/583) ([mattrobenolt](https://github.com/mattrobenolt))
- Allow inactive users to login [\#580](https://github.com/omab/python-social-auth/pull/580) ([LucasRoesler](https://github.com/LucasRoesler))
- Update LICENSE [\#573](https://github.com/omab/python-social-auth/pull/573) ([yasoob](https://github.com/yasoob))

## [v0.2.3](https://github.com/omab/python-social-auth/tree/v0.2.3) (2015-03-31)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.2...v0.2.3)

**Closed issues:**

- get\_username as a classmethod collides with the standard django implementation and other packages [\#564](https://github.com/omab/python-social-auth/issues/564)
- Make it easier to disable social\_details pipeline step [\#555](https://github.com/omab/python-social-auth/issues/555)
- Not compatible with requests-oauthlib 0.3.0 [\#545](https://github.com/omab/python-social-auth/issues/545)
- how to remove "redirect\_state" params? \( Kakao OAuth2 Error \) [\#538](https://github.com/omab/python-social-auth/issues/538)
- async interface for models in tornado [\#535](https://github.com/omab/python-social-auth/issues/535)
- `social.strategies.django\_strategy` work with django 1.7.4  "This QueryDict instance is immutable" [\#528](https://github.com/omab/python-social-auth/issues/528)
- Update PyPI [\#523](https://github.com/omab/python-social-auth/issues/523)
- Missing migration [\#516](https://github.com/omab/python-social-auth/issues/516)
- Not getting correct GoogleOath2 details when signing up by OAuth access token [\#499](https://github.com/omab/python-social-auth/issues/499)
- Jawbone backend problem, AuthCanceled exception. [\#497](https://github.com/omab/python-social-auth/issues/497)
- StravaOAuth - Strava authentication backend not working. [\#455](https://github.com/omab/python-social-auth/issues/455)

**Merged pull requests:**

- Added NaszaKlasa OAuth2 support [\#570](https://github.com/omab/python-social-auth/pull/570) ([hoffmannkrzysztof](https://github.com/hoffmannkrzysztof))
- Add revoke token ability to strava [\#569](https://github.com/omab/python-social-auth/pull/569) ([buddylindsey](https://github.com/buddylindsey))
- set redirect\_state to false for live oauth2 [\#563](https://github.com/omab/python-social-auth/pull/563) ([wj1918](https://github.com/wj1918))
- Khan academy backend user\_id is required to use any further requests [\#561](https://github.com/omab/python-social-auth/pull/561) ([aniav](https://github.com/aniav))
- Rednose and config [\#560](https://github.com/omab/python-social-auth/pull/560) ([jeromelefeuvre](https://github.com/jeromelefeuvre))
- Add missing migration for Django app [\#558](https://github.com/omab/python-social-auth/pull/558) ([andreipetre](https://github.com/andreipetre))
- Require PyJWT\>=1.0.0,\<2.0.0 [\#557](https://github.com/omab/python-social-auth/pull/557) ([jpadilla](https://github.com/jpadilla))
- Start pipeline with default details arg [\#556](https://github.com/omab/python-social-auth/pull/556) ([johtso](https://github.com/johtso))
- Add `python\_chameleon` to setup [\#554](https://github.com/omab/python-social-auth/pull/554) ([jeromelefeuvre](https://github.com/jeromelefeuvre))
- update for django 1.9 [\#550](https://github.com/omab/python-social-auth/pull/550) ([DanielJDufour](https://github.com/DanielJDufour))
- Added support for Vend [\#549](https://github.com/omab/python-social-auth/pull/549) ([matthowland](https://github.com/matthowland))
- Increase min request-oauthlib version to 0.3.1 [\#548](https://github.com/omab/python-social-auth/pull/548) ([johtso](https://github.com/johtso))
- Add wunderlist backend to the list [\#547](https://github.com/omab/python-social-auth/pull/547) ([bogdal](https://github.com/bogdal))
- Typo in index.html [\#544](https://github.com/omab/python-social-auth/pull/544) ([flesser](https://github.com/flesser))
- Wunderlist oauth2 backend [\#543](https://github.com/omab/python-social-auth/pull/543) ([bogdal](https://github.com/bogdal))
- Add backend for EVE Online Single Sign-On \(OAuth2\) [\#541](https://github.com/omab/python-social-auth/pull/541) ([flesser](https://github.com/flesser))
- Add extra info on Google+ Sign-In doc [\#540](https://github.com/omab/python-social-auth/pull/540) ([Menda](https://github.com/Menda))
- fix issue \#538 : disable redirect\_state on KakaoOAuth2 [\#539](https://github.com/omab/python-social-auth/pull/539) ([dobestan](https://github.com/dobestan))
- Update google.rst [\#537](https://github.com/omab/python-social-auth/pull/537) ([tclancy](https://github.com/tclancy))
- Added Yahoo OAuth2 support [\#536](https://github.com/omab/python-social-auth/pull/536) ([hassek](https://github.com/hassek))
- Fix Issue \#532 [\#533](https://github.com/omab/python-social-auth/pull/533) ([littlezz](https://github.com/littlezz))

## [v0.2.2](https://github.com/omab/python-social-auth/tree/v0.2.2) (2015-02-23)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.1...v0.2.2)

**Closed issues:**

- Problem with REQUEST in Django 1.7 [\#508](https://github.com/omab/python-social-auth/issues/508)
- Unique constraint on nonce missing [\#490](https://github.com/omab/python-social-auth/issues/490)
- AuthStateMissing [\#462](https://github.com/omab/python-social-auth/issues/462)
- \<django.utils.functional.lazy.\<locals\>.\_\_proxy\_\_ object at 0x7feb8a56f5f8\> is not JSON serializable [\#460](https://github.com/omab/python-social-auth/issues/460)
- Cannot import name migrations [\#456](https://github.com/omab/python-social-auth/issues/456)
- Bugs in tornado\_strategy.py [\#445](https://github.com/omab/python-social-auth/issues/445)
- Cannot login with social account anymore after migration from DSA \(but association is OK\) [\#444](https://github.com/omab/python-social-auth/issues/444)
- Mode debug [\#443](https://github.com/omab/python-social-auth/issues/443)
- On linkedin,github login: AttributeError at http://llovebaimuda.herokuapp.com:8000/complete/github/ 'GithubBackend' object has no attribute 'auth\_allowed' [\#441](https://github.com/omab/python-social-auth/issues/441)
- Can not migrate database with django 1.7 [\#439](https://github.com/omab/python-social-auth/issues/439)
- AuthAlreadyAssociated at /complete/google-oauth2/ [\#437](https://github.com/omab/python-social-auth/issues/437)
- Python social auth redirect to LOGIN\_ERROR [\#435](https://github.com/omab/python-social-auth/issues/435)
- Can't register user when using email as username [\#434](https://github.com/omab/python-social-auth/issues/434)
- Problems connecting Google OAUTH2 [\#433](https://github.com/omab/python-social-auth/issues/433)
- Can't get refresh\_token from google-oauth2 response [\#431](https://github.com/omab/python-social-auth/issues/431)
- UserMixin.tokens naming [\#430](https://github.com/omab/python-social-auth/issues/430)
- Django 1.7 Type Object 'Migration' has no Attribute 'models' [\#427](https://github.com/omab/python-social-auth/issues/427)
- Django 1.7 warning - You have unapplied migrations [\#426](https://github.com/omab/python-social-auth/issues/426)
- Should the Django app's auth view be cacheable? [\#425](https://github.com/omab/python-social-auth/issues/425)
- changelog 0.2.1 only vs. releases on github 0.2.0 only [\#421](https://github.com/omab/python-social-auth/issues/421)
- Don't know how to redirect to right redirect\_uri. Use gunicorn + nginx + django1.7 [\#420](https://github.com/omab/python-social-auth/issues/420)
- Request object not passed in pipeline [\#419](https://github.com/omab/python-social-auth/issues/419)
- How to save the user data.? [\#418](https://github.com/omab/python-social-auth/issues/418)
- GitHub doesn't select Primary Email [\#413](https://github.com/omab/python-social-auth/issues/413)
- Unwanted and forced use of Google+ API for signin [\#406](https://github.com/omab/python-social-auth/issues/406)
- Renaming social url namespace [\#399](https://github.com/omab/python-social-auth/issues/399)
- How to overwrite redirect\_uri? [\#383](https://github.com/omab/python-social-auth/issues/383)
- GoogleOauth2 hangs mod\_wsgi after multiple logins. [\#377](https://github.com/omab/python-social-auth/issues/377)
- Facebook /login/facebook-app/ printing None [\#376](https://github.com/omab/python-social-auth/issues/376)
- How to test a custom python-social-auth pipeline? [\#352](https://github.com/omab/python-social-auth/issues/352)
- Cannot figure out how to associate multiple auth providers [\#340](https://github.com/omab/python-social-auth/issues/340)
- No user param in partial pipeline function [\#323](https://github.com/omab/python-social-auth/issues/323)

**Merged pull requests:**

- Fix example of pyramid [\#529](https://github.com/omab/python-social-auth/pull/529) ([narusemotoki](https://github.com/narusemotoki))
- fix python3 handling of openid backend on sqlalchemy storage [\#524](https://github.com/omab/python-social-auth/pull/524) ([ghost](https://github.com/ghost))
- Don't use "import" in example method paths docs to avoid confusion [\#521](https://github.com/omab/python-social-auth/pull/521) ([lamby](https://github.com/lamby))
- Add dribbble backend. [\#519](https://github.com/omab/python-social-auth/pull/519) ([tell-k](https://github.com/tell-k))
- Fixed issue: GET dictionary is immutable. [\#518](https://github.com/omab/python-social-auth/pull/518) ([baroale](https://github.com/baroale))
- Include username in Reddit extra\_data [\#517](https://github.com/omab/python-social-auth/pull/517) ([chris-martin](https://github.com/chris-martin))
- \[facebook-oauth2\] Verifying Graph API Calls with appsecret\_proof [\#515](https://github.com/omab/python-social-auth/pull/515) ([eagafonov](https://github.com/eagafonov))
- Add Zotero Backend [\#514](https://github.com/omab/python-social-auth/pull/514) ([cdeblois](https://github.com/cdeblois))
- add qiita backend [\#512](https://github.com/omab/python-social-auth/pull/512) ([tell-k](https://github.com/tell-k))
- Fix: Issue \#508 [\#511](https://github.com/omab/python-social-auth/pull/511) ([baroale](https://github.com/baroale))
- Fix Google documentation [\#510](https://github.com/omab/python-social-auth/pull/510) ([Menda](https://github.com/Menda))
- Updated PyJWT Dependency [\#509](https://github.com/omab/python-social-auth/pull/509) ([clintonb](https://github.com/clintonb))
- Ensure email is not None [\#503](https://github.com/omab/python-social-auth/pull/503) ([ianw](https://github.com/ianw))
- Pull Request for \#501 [\#502](https://github.com/omab/python-social-auth/pull/502) ([cdeblois](https://github.com/cdeblois))
- Add support for Launchpad OpenId [\#500](https://github.com/omab/python-social-auth/pull/500) ([ianw](https://github.com/ianw))
- Jawbone authentification fix [\#498](https://github.com/omab/python-social-auth/pull/498) ([rivf](https://github.com/rivf))
- Coursera backend [\#496](https://github.com/omab/python-social-auth/pull/496) ([adambabik](https://github.com/adambabik))
- Added nonce unique constraint [\#491](https://github.com/omab/python-social-auth/pull/491) ([candlejack297](https://github.com/candlejack297))
- Store Spotify's refresh\_token. [\#482](https://github.com/omab/python-social-auth/pull/482) ([ctbarna](https://github.com/ctbarna))
- Slack improvements [\#479](https://github.com/omab/python-social-auth/pull/479) ([gorillamania](https://github.com/gorillamania))
- Fixed extra\_data field in django 1.7 initial migration [\#476](https://github.com/omab/python-social-auth/pull/476) ([bendavis78](https://github.com/bendavis78))
- YahooOAuth failed to get primary email if multiple email found in the profile. [\#473](https://github.com/omab/python-social-auth/pull/473) ([wj1918](https://github.com/wj1918))
- Update base.py [\#472](https://github.com/omab/python-social-auth/pull/472) ([travoltino](https://github.com/travoltino))
- Slack backend [\#471](https://github.com/omab/python-social-auth/pull/471) ([gorillamania](https://github.com/gorillamania))
- Update GitHub documentation [\#469](https://github.com/omab/python-social-auth/pull/469) ([alexmuller](https://github.com/alexmuller))
- Fix \#460: Call force\_text on \_URL settings to support reverse\_lazy with default session serializer [\#468](https://github.com/omab/python-social-auth/pull/468) ([frankier](https://github.com/frankier))
- Update Django instructions to fix South migrations [\#454](https://github.com/omab/python-social-auth/pull/454) ([drpancake](https://github.com/drpancake))
- Added backend for professionali.ru [\#452](https://github.com/omab/python-social-auth/pull/452) ([kblw](https://github.com/kblw))
- Removed Orkut backend [\#450](https://github.com/omab/python-social-auth/pull/450) ([lukasklein](https://github.com/lukasklein))
- Allow the pipeline to change the redirect url. [\#449](https://github.com/omab/python-social-auth/pull/449) ([tim-schilling](https://github.com/tim-schilling))
- Added support for Django's User.EMAIL\_FIELD. [\#447](https://github.com/omab/python-social-auth/pull/447) ([SeanHayes](https://github.com/SeanHayes))
- Khan Academy backend [\#446](https://github.com/omab/python-social-auth/pull/446) ([aniav](https://github.com/aniav))
- Fix typo for AUTH\_USER\_MODEL [\#432](https://github.com/omab/python-social-auth/pull/432) ([jlynn](https://github.com/jlynn))
- Update base.py , removing unncessary code after refactoring [\#429](https://github.com/omab/python-social-auth/pull/429) ([aparij](https://github.com/aparij))
- use correct tense for `to meet' [\#428](https://github.com/omab/python-social-auth/pull/428) ([mgalgs](https://github.com/mgalgs))
- Fix custom user model migrations for Django 1.7 [\#422](https://github.com/omab/python-social-auth/pull/422) ([jlynn](https://github.com/jlynn))
- Fix migration issue on python 3 [\#417](https://github.com/omab/python-social-auth/pull/417) ([EnTeQuAk](https://github.com/EnTeQuAk))
- Fix does not match the number of arguments \(for vk and ok backend\) [\#415](https://github.com/omab/python-social-auth/pull/415) ([silentsokolov](https://github.com/silentsokolov))
- Salesforce OAuth2 support [\#412](https://github.com/omab/python-social-auth/pull/412) ([postrational](https://github.com/postrational))
- Thedrow patch 1 [\#411](https://github.com/omab/python-social-auth/pull/411) ([omab](https://github.com/omab))
- Added Python 3.4 and PyPy to the build matrix. [\#410](https://github.com/omab/python-social-auth/pull/410) ([thedrow](https://github.com/thedrow))
- Added Django 1.7 App Config [\#409](https://github.com/omab/python-social-auth/pull/409) ([micahhausler](https://github.com/micahhausler))
- Django admin enhancements  [\#408](https://github.com/omab/python-social-auth/pull/408) ([micahhausler](https://github.com/micahhausler))
- Use new GoogleOAuth2 Spec [\#407](https://github.com/omab/python-social-auth/pull/407) ([jaitaiwan](https://github.com/jaitaiwan))
- \[flask\_example\_app\]: Incorrect import path for db model [\#405](https://github.com/omab/python-social-auth/pull/405) ([labeneator](https://github.com/labeneator))
- Add Kakao link and detailed address for description. [\#403](https://github.com/omab/python-social-auth/pull/403) ([jeyraof](https://github.com/jeyraof))
- Added some legal stuff [\#402](https://github.com/omab/python-social-auth/pull/402) ([dzerrenner](https://github.com/dzerrenner))
- Recreate migration with Django 1.7 final and re-PEP8. [\#401](https://github.com/omab/python-social-auth/pull/401) ([akx](https://github.com/akx))
- master  add SCOPE\_SEPARATOR to DisqusOAuth2 [\#398](https://github.com/omab/python-social-auth/pull/398) ([vero4karu](https://github.com/vero4karu))
- added a backend for Battle.net Oauth2 auth [\#397](https://github.com/omab/python-social-auth/pull/397) ([dzerrenner](https://github.com/dzerrenner))
- Update documentation with info on upgrading from 0.1-0.2 with migrations [\#395](https://github.com/omab/python-social-auth/pull/395) ([timsavage](https://github.com/timsavage))
- Allow more Trello settings [\#389](https://github.com/omab/python-social-auth/pull/389) ([sk7](https://github.com/sk7))
- Updated to use latest api wrapper [\#386](https://github.com/omab/python-social-auth/pull/386) ([dhendo](https://github.com/dhendo))
- updated the docs to add migrations for 1.7 while updated a constant so the warning message does not appear when running command line [\#382](https://github.com/omab/python-social-auth/pull/382) ([masterfung](https://github.com/masterfung))
- Jawbone needs params instead of data as requests [\#380](https://github.com/omab/python-social-auth/pull/380) ([amolkher](https://github.com/amolkher))
- Don't overwrite clean\_kwargs with kwargs [\#332](https://github.com/omab/python-social-auth/pull/332) ([cambridgemike](https://github.com/cambridgemike))
- Reinstated get\_user\_id override [\#314](https://github.com/omab/python-social-auth/pull/314) ([dhendo](https://github.com/dhendo))
- Update django\_orm.py [\#312](https://github.com/omab/python-social-auth/pull/312) ([synotna](https://github.com/synotna))

## [v0.2.1](https://github.com/omab/python-social-auth/tree/v0.2.1) (2014-09-11)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.2.0...v0.2.1)

## [v0.2.0](https://github.com/omab/python-social-auth/tree/v0.2.0) (2014-09-11)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.26...v0.2.0)

**Closed issues:**

- cannot import name strategy [\#370](https://github.com/omab/python-social-auth/issues/370)
- Request object has no attribute 'backend' in SocialAuthExceptionMiddleware [\#369](https://github.com/omab/python-social-auth/issues/369)
- Shopify Backend [\#368](https://github.com/omab/python-social-auth/issues/368)
- State parameter incorrectly missing for some backends [\#367](https://github.com/omab/python-social-auth/issues/367)
- /signup/email/ instead of /login/email/ [\#366](https://github.com/omab/python-social-auth/issues/366)
- Improve pipeline documentation [\#361](https://github.com/omab/python-social-auth/issues/361)
- request: opposite default behavior for SOCIAL\_AUTH\_SESSION\_EXPIRATION [\#356](https://github.com/omab/python-social-auth/issues/356)
- after installing I have got an error: ImportError: No module named defaultqrcode [\#355](https://github.com/omab/python-social-auth/issues/355)
- SocialAuthExceptionMiddleware raises AttributeError [\#350](https://github.com/omab/python-social-auth/issues/350)
- Python 3 support [\#349](https://github.com/omab/python-social-auth/issues/349)
- can I set redirect\_uri use weibo backend? [\#345](https://github.com/omab/python-social-auth/issues/345)
- Toronodo-Facebook oauth [\#342](https://github.com/omab/python-social-auth/issues/342)
- Security issue with Twitter backend - state parameter [\#338](https://github.com/omab/python-social-auth/issues/338)
- \<mis-submit\> [\#330](https://github.com/omab/python-social-auth/issues/330)
- Github support for checking if a user is part of a team [\#329](https://github.com/omab/python-social-auth/issues/329)
- Github OAuth2 backend fails with 404 when retrieving access token [\#327](https://github.com/omab/python-social-auth/issues/327)
- django admin User social auth search broken [\#322](https://github.com/omab/python-social-auth/issues/322)
- Script to migrate django sessions to python social auth  [\#320](https://github.com/omab/python-social-auth/issues/320)
- Error with facebook login [\#315](https://github.com/omab/python-social-auth/issues/315)
- NotImplementedError [\#310](https://github.com/omab/python-social-auth/issues/310)
- No module named 'social\_auth' on social/utils.py [\#306](https://github.com/omab/python-social-auth/issues/306)
- What is the correct way to use get tokens with GooglePlus? [\#305](https://github.com/omab/python-social-auth/issues/305)
- custom LOGIN\_REDIRECT\_URL per backend [\#301](https://github.com/omab/python-social-auth/issues/301)
- Instagram has changed user data format [\#296](https://github.com/omab/python-social-auth/issues/296)
- Getting "cannot import name psa" error [\#295](https://github.com/omab/python-social-auth/issues/295)
- Broken partial auth with Django and 0.1.24 [\#291](https://github.com/omab/python-social-auth/issues/291)
- Google+ Sign-in problem [\#285](https://github.com/omab/python-social-auth/issues/285)
- AuthStateMissing: Session value state missing [\#279](https://github.com/omab/python-social-auth/issues/279)
- Always returns me detail: "Invalid token" [\#268](https://github.com/omab/python-social-auth/issues/268)
- On facebook login: AttributeError at /complete/facebook/ 'NoneType' object has no attribute 'expiration\_datetime' [\#190](https://github.com/omab/python-social-auth/issues/190)

**Merged pull requests:**

- Adds backend for MineID.org [\#379](https://github.com/omab/python-social-auth/pull/379) ([caioariede](https://github.com/caioariede))
- Fix typo [\#372](https://github.com/omab/python-social-auth/pull/372) ([gipi](https://github.com/gipi))
- Updated OpenId Connect Test Mixin [\#371](https://github.com/omab/python-social-auth/pull/371) ([clintonb](https://github.com/clintonb))
- Small grammatical edit [\#363](https://github.com/omab/python-social-auth/pull/363) ([x0xMaximus](https://github.com/x0xMaximus))
- Fix repository links in thanks document. [\#359](https://github.com/omab/python-social-auth/pull/359) ([martey](https://github.com/martey))
- changed default behavior of SESSION\_EXPIRATION setting [\#358](https://github.com/omab/python-social-auth/pull/358) ([gameguy43](https://github.com/gameguy43))
- added goclio oauth2 backend [\#357](https://github.com/omab/python-social-auth/pull/357) ([rosscdh](https://github.com/rosscdh))
- Add pushbullet backends [\#351](https://github.com/omab/python-social-auth/pull/351) ([ralmn](https://github.com/ralmn))
- Added Open ID Connect base backend [\#348](https://github.com/omab/python-social-auth/pull/348) ([clintonb](https://github.com/clintonb))
- numeric index for format [\#347](https://github.com/omab/python-social-auth/pull/347) ([jprobst21](https://github.com/jprobst21))
- Update vk.rst [\#341](https://github.com/omab/python-social-auth/pull/341) ([darthwade](https://github.com/darthwade))
- Django \<1.7 Migration Support [\#339](https://github.com/omab/python-social-auth/pull/339) ([mhluongo](https://github.com/mhluongo))
- Strava name population fixes [\#336](https://github.com/omab/python-social-auth/pull/336) ([lamby](https://github.com/lamby))
- Correct Strava scoping/permissions example. [\#335](https://github.com/omab/python-social-auth/pull/335) ([lamby](https://github.com/lamby))
- Clean up language in social/tests/README.rst [\#334](https://github.com/omab/python-social-auth/pull/334) ([chris-martin](https://github.com/chris-martin))
- Fixed \#327 -- Changed access token method on backend. [\#328](https://github.com/omab/python-social-auth/pull/328) ([slurms](https://github.com/slurms))
- Minor doc updates [\#326](https://github.com/omab/python-social-auth/pull/326) ([seizethedave](https://github.com/seizethedave))
- fix for AssertionError in pyramid [\#319](https://github.com/omab/python-social-auth/pull/319) ([marinewater](https://github.com/marinewater))
- Added Django 1.7 migrations [\#318](https://github.com/omab/python-social-auth/pull/318) ([ondrowan](https://github.com/ondrowan))
- reddit sometimes responds with "429 Too Many Requests" seemingly randomly [\#317](https://github.com/omab/python-social-auth/pull/317) ([davidhubbard](https://github.com/davidhubbard))
- Update link to Django example in documentation. [\#311](https://github.com/omab/python-social-auth/pull/311) ([martey](https://github.com/martey))
- Add note about access\_type in docs [\#308](https://github.com/omab/python-social-auth/pull/308) ([romanlevin](https://github.com/romanlevin))
- The Moves app backend [\#307](https://github.com/omab/python-social-auth/pull/307) ([avibrazil](https://github.com/avibrazil))
- QQ backend [\#302](https://github.com/omab/python-social-auth/pull/302) ([omab](https://github.com/omab))
- \[documentation\] text should not go into code block [\#299](https://github.com/omab/python-social-auth/pull/299) ([GabLeRoux](https://github.com/GabLeRoux))
- Vkotnakte [\#298](https://github.com/omab/python-social-auth/pull/298) ([freydev](https://github.com/freydev))
- Update docker backend with Docker Hub endpoints [\#293](https://github.com/omab/python-social-auth/pull/293) ([jlhawn](https://github.com/jlhawn))

## [v0.1.26](https://github.com/omab/python-social-auth/tree/v0.1.26) (2014-06-07)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.25...v0.1.26)

**Closed issues:**

- Google OAuth2 broken since 0.1.24 [\#292](https://github.com/omab/python-social-auth/issues/292)

## [v0.1.25](https://github.com/omab/python-social-auth/tree/v0.1.25) (2014-06-07)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.24...v0.1.25)

**Closed issues:**

- LinkedIn-OAuth2 refresh\_token doesn't work  [\#289](https://github.com/omab/python-social-auth/issues/289)
- Process exceptions even when DEBUG = True [\#287](https://github.com/omab/python-social-auth/issues/287)
- python-openid does not support py3k. Alternatives? [\#282](https://github.com/omab/python-social-auth/issues/282)
- Twitter OAuth using access\_token [\#272](https://github.com/omab/python-social-auth/issues/272)

**Merged pull requests:**

- Rdio API methods use POST [\#288](https://github.com/omab/python-social-auth/pull/288) ([dasevilla](https://github.com/dasevilla))
- Fixed Django 1.7 admin [\#286](https://github.com/omab/python-social-auth/pull/286) ([godshall](https://github.com/godshall))
- avoid updating default settings [\#281](https://github.com/omab/python-social-auth/pull/281) ([l-hedgehog](https://github.com/l-hedgehog))

## [v0.1.24](https://github.com/omab/python-social-auth/tree/v0.1.24) (2014-05-18)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.23...v0.1.24)

**Closed issues:**

- Facebook2OAuth2 not setting 'client\_id' parameter when redirecting to login [\#280](https://github.com/omab/python-social-auth/issues/280)
- Wrong version on pip [\#277](https://github.com/omab/python-social-auth/issues/277)
- SOCIAL\_AUTH\_NEW\_USER\_REDIRECT\_URL strange behaviour [\#276](https://github.com/omab/python-social-auth/issues/276)
- Feature request: Ability to encrypt access tokens [\#274](https://github.com/omab/python-social-auth/issues/274)
- Google is deprecating some OAuth scopes [\#273](https://github.com/omab/python-social-auth/issues/273)
- 'RegexURLResolver' object has no attribute '\_urlconf\_module' [\#269](https://github.com/omab/python-social-auth/issues/269)
- I am facing a 500: Internal Server Error after clicking any link  [\#266](https://github.com/omab/python-social-auth/issues/266)
- EXTRA\_DATA for VK [\#263](https://github.com/omab/python-social-auth/issues/263)
- Amazon Docs Out of Date? [\#260](https://github.com/omab/python-social-auth/issues/260)
- Strava Integration OAuth Redirect Issue [\#259](https://github.com/omab/python-social-auth/issues/259)
- Add the ability to customize AX\_SCHEMA\_ATTRS [\#258](https://github.com/omab/python-social-auth/issues/258)
- g.user may be Proxy! \(flask bug\) [\#257](https://github.com/omab/python-social-auth/issues/257)
- Error running syncdb with MySQL utf8mb4 charset [\#255](https://github.com/omab/python-social-auth/issues/255)
- Use of Django Internal Property [\#254](https://github.com/omab/python-social-auth/issues/254)
- Persona auth failing to authenticate when using a custom user model \[Django\] [\#253](https://github.com/omab/python-social-auth/issues/253)
- Facebook: "Invalid App ID: None" [\#252](https://github.com/omab/python-social-auth/issues/252)
- "vk-openapi" backend error [\#250](https://github.com/omab/python-social-auth/issues/250)
- request hanging after social authentication [\#248](https://github.com/omab/python-social-auth/issues/248)
- Unable To Redirect User After Facebook Authentication [\#247](https://github.com/omab/python-social-auth/issues/247)
- social.exceptions.AuthStateMissing [\#244](https://github.com/omab/python-social-auth/issues/244)
- Facebook Re-authentication [\#243](https://github.com/omab/python-social-auth/issues/243)
- SOCIAL\_AUTH\_DEFAULT\_USERNAME [\#241](https://github.com/omab/python-social-auth/issues/241)
- Refactor first, last and full name population [\#240](https://github.com/omab/python-social-auth/issues/240)
- Authication using acees token works for facebook but not twitter and VK [\#238](https://github.com/omab/python-social-auth/issues/238)
- MendeleyOAuth2 does not require REDIRECT\_STATE [\#234](https://github.com/omab/python-social-auth/issues/234)
- Autnticate/Create user from acces\_token  [\#233](https://github.com/omab/python-social-auth/issues/233)
- Problem using @partial with GoogleOpenId in Django 1.6 and python 3.3 [\#231](https://github.com/omab/python-social-auth/issues/231)
- Unicode error with UTF-8 string in next [\#229](https://github.com/omab/python-social-auth/issues/229)
- Error with "Enhanced redirection security" in Microsoft account \(Live backend\). [\#218](https://github.com/omab/python-social-auth/issues/218)

**Merged pull requests:**

- Implementing Spotify and Beats OAuth implementations. [\#283](https://github.com/omab/python-social-auth/pull/283) ([ryankicks](https://github.com/ryankicks))
- Add MapMyFitness [\#278](https://github.com/omab/python-social-auth/pull/278) ([JasonSanford](https://github.com/JasonSanford))
- from http API to https API [\#275](https://github.com/omab/python-social-auth/pull/275) ([swmerko](https://github.com/swmerko))
- Replace references to python-oauth2 with references to requests-oauthlib [\#271](https://github.com/omab/python-social-auth/pull/271) ([malept](https://github.com/malept))
- get email on login via VK [\#267](https://github.com/omab/python-social-auth/pull/267) ([Smamaxs](https://github.com/Smamaxs))
- Change the authorization url for the xing api [\#265](https://github.com/omab/python-social-auth/pull/265) ([hujiko](https://github.com/hujiko))
- Support for Facebook Open Graph 2.0 [\#264](https://github.com/omab/python-social-auth/pull/264) ([dryan](https://github.com/dryan))
- Added LoginRadius backend. [\#262](https://github.com/omab/python-social-auth/pull/262) ([grepme](https://github.com/grepme))
- Add Kakao backend [\#261](https://github.com/omab/python-social-auth/pull/261) ([momamene](https://github.com/momamene))
- Using https as required by the API [\#256](https://github.com/omab/python-social-auth/pull/256) ([gmist](https://github.com/gmist))
- User model fields accessors clashes issue solved [\#251](https://github.com/omab/python-social-auth/pull/251) ([wumzi](https://github.com/wumzi))
- linkedin now requires redirect uris to be verified: https://developer.li... [\#246](https://github.com/omab/python-social-auth/pull/246) ([dblado](https://github.com/dblado))
- Add Twitch backend [\#245](https://github.com/omab/python-social-auth/pull/245) ([hannseman](https://github.com/hannseman))
- Handle properly refusing when entering via twitter [\#242](https://github.com/omab/python-social-auth/pull/242) ([Chern](https://github.com/Chern))
- Fix small spelling mistake. [\#239](https://github.com/omab/python-social-auth/pull/239) ([cdepillabout](https://github.com/cdepillabout))
- Add support for Vimeo OAuth 2 as part of Vimeo API v3 [\#237](https://github.com/omab/python-social-auth/pull/237) ([jjshabs](https://github.com/jjshabs))
- Update settings.rst [\#236](https://github.com/omab/python-social-auth/pull/236) ([krishangupta](https://github.com/krishangupta))
- Incorrect syntax given in the documention [\#235](https://github.com/omab/python-social-auth/pull/235) ([mdamien](https://github.com/mdamien))
- login with bitbucket account, error when any verified email is set [\#230](https://github.com/omab/python-social-auth/pull/230) ([pekoslaw](https://github.com/pekoslaw))

## [v0.1.23](https://github.com/omab/python-social-auth/tree/v0.1.23) (2014-03-26)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.22...v0.1.23)

**Closed issues:**

- Handling AuthAlreadyAssociated [\#226](https://github.com/omab/python-social-auth/issues/226)
- AuthFailed at /complete/dropbox-oauth2/ [\#225](https://github.com/omab/python-social-auth/issues/225)
- Github says 404 when I want to use it [\#224](https://github.com/omab/python-social-auth/issues/224)
- Dropbox OAuth2 backend not found [\#223](https://github.com/omab/python-social-auth/issues/223)
- EmailAuth pipeline - saving password [\#222](https://github.com/omab/python-social-auth/issues/222)
- SocialAuthExceptionMiddleware is not thread safe. [\#221](https://github.com/omab/python-social-auth/issues/221)
- `AuthStateMissing` and `HTTPError` being raised [\#220](https://github.com/omab/python-social-auth/issues/220)
- Saving to session and access after pipeline [\#219](https://github.com/omab/python-social-auth/issues/219)
- Migrating from Django social auth [\#214](https://github.com/omab/python-social-auth/issues/214)
- No module named apps.django\_app.default.models in custom pipeline [\#213](https://github.com/omab/python-social-auth/issues/213)
- complete login with facebook app [\#212](https://github.com/omab/python-social-auth/issues/212)
- Use Django messages in SocialAuthExceptionMiddleware even for anonymous users [\#210](https://github.com/omab/python-social-auth/issues/210)
- HTTPError at /complete/facebook/ when trying to connect to Facebook. [\#207](https://github.com/omab/python-social-auth/issues/207)
- Steam backend not using stateless mode [\#200](https://github.com/omab/python-social-auth/issues/200)
- Got UnicodeEncodeError when redirection parameter &next=/apage/contains/inτερnαtιοnal/characters/ [\#191](https://github.com/omab/python-social-auth/issues/191)
- PIP install to virtual environment fails [\#177](https://github.com/omab/python-social-auth/issues/177)
- AUTHENTICATION\_BACKENDS [\#131](https://github.com/omab/python-social-auth/issues/131)

**Merged pull requests:**

- Added backend for Last.Fm. [\#232](https://github.com/omab/python-social-auth/pull/232) ([eriklavander](https://github.com/eriklavander))
- Added Docker.io backend [\#228](https://github.com/omab/python-social-auth/pull/228) ([fermayo](https://github.com/fermayo))
- OpenStreetMap: no img element if user has no avatar [\#227](https://github.com/omab/python-social-auth/pull/227) ([yohanboniface](https://github.com/yohanboniface))
- Added support for strava [\#217](https://github.com/omab/python-social-auth/pull/217) ([abunsen](https://github.com/abunsen))
- Removes flask dependency from webpy\_app [\#216](https://github.com/omab/python-social-auth/pull/216) ([w0rm](https://github.com/w0rm))
- Added backend for Ubuntu \(One\). [\#215](https://github.com/omab/python-social-auth/pull/215) ([schwuk](https://github.com/schwuk))
- Fixed Django \< 1.4 support in context processors. [\#211](https://github.com/omab/python-social-auth/pull/211) ([bmispelon](https://github.com/bmispelon))
- Add some missing test dependencies for `social.apps.django\_app.default.tests` [\#209](https://github.com/omab/python-social-auth/pull/209) ([pzrq](https://github.com/pzrq))

## [v0.1.22](https://github.com/omab/python-social-auth/tree/v0.1.22) (2014-03-01)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.21...v0.1.22)

**Closed issues:**

- Email confirmation is broken for SQLAlchemy storage and webpy\_app [\#204](https://github.com/omab/python-social-auth/issues/204)
- Associate by mail doesn't return is\_new flag [\#201](https://github.com/omab/python-social-auth/issues/201)
- Coinbase backend defaults to 'balance' but the complete calls user\_data with looks for /users api path [\#199](https://github.com/omab/python-social-auth/issues/199)
- Partial pipeline doesn't restore user model [\#198](https://github.com/omab/python-social-auth/issues/198)
- mongoengine should support USERNAME\_FIELD ? [\#197](https://github.com/omab/python-social-auth/issues/197)
- Action of do\_complete is not managing exceptions thrown during strategy.complete [\#196](https://github.com/omab/python-social-auth/issues/196)
- Using Django-facebook side by side [\#195](https://github.com/omab/python-social-auth/issues/195)
- Saving user as inactive in a pipeline, causes redirect to login error [\#194](https://github.com/omab/python-social-auth/issues/194)
- case-sensetive ?next= parameter dont work [\#193](https://github.com/omab/python-social-auth/issues/193)
- TypeError: can only concatenate list \(not "str"\) to list [\#186](https://github.com/omab/python-social-auth/issues/186)
- Post-authentication redirects: are they still supported? [\#182](https://github.com/omab/python-social-auth/issues/182)
- LinkedIn HTTPError: 401 Client Error: Unauthorized [\#181](https://github.com/omab/python-social-auth/issues/181)
- How to register user by access\_token [\#180](https://github.com/omab/python-social-auth/issues/180)
- Session value state missing [\#166](https://github.com/omab/python-social-auth/issues/166)
- Unavailable facebook raises unexpected ConnectionError [\#155](https://github.com/omab/python-social-auth/issues/155)
- Exceptions not noted in logs [\#154](https://github.com/omab/python-social-auth/issues/154)
- Internal Server Error: /complete/facebook/ -\> raise KeyError [\#153](https://github.com/omab/python-social-auth/issues/153)
- Migrating server [\#128](https://github.com/omab/python-social-auth/issues/128)
- django example: trying to get only the email auth work for now... [\#118](https://github.com/omab/python-social-auth/issues/118)
- Can we choose to set the login url escaped ? [\#115](https://github.com/omab/python-social-auth/issues/115)
- Incorporating rauth? [\#3](https://github.com/omab/python-social-auth/issues/3)

**Merged pull requests:**

- Fixes broken email confirmation for SQLAlchemy storage and webpy\_app [\#205](https://github.com/omab/python-social-auth/pull/205) ([w0rm](https://github.com/w0rm))
- Update mendeley.py [\#203](https://github.com/omab/python-social-auth/pull/203) ([sbassi](https://github.com/sbassi))
- Removed commit marker [\#192](https://github.com/omab/python-social-auth/pull/192) ([dkingman](https://github.com/dkingman))
- Add Clef backend [\#189](https://github.com/omab/python-social-auth/pull/189) ([tklovett](https://github.com/tklovett))
- Fixed a typo. [\#188](https://github.com/omab/python-social-auth/pull/188) ([ykalchevskiy](https://github.com/ykalchevskiy))
- Add a Bitdeli Badge to README [\#185](https://github.com/omab/python-social-auth/pull/185) ([bitdeli-chef](https://github.com/bitdeli-chef))
- added information for FIELDS\_STORED\_IN\_SESSION [\#184](https://github.com/omab/python-social-auth/pull/184) ([joelewis](https://github.com/joelewis))
- updated live connection for better support [\#183](https://github.com/omab/python-social-auth/pull/183) ([hassek](https://github.com/hassek))

## [v0.1.21](https://github.com/omab/python-social-auth/tree/v0.1.21) (2014-02-05)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.20...v0.1.21)

**Closed issues:**

- User association by email should be case insensitive [\#179](https://github.com/omab/python-social-auth/issues/179)
- ImproperlyConfigured: Module "social.apps.django\_app.utils" does not define a "BackendWrapper" authentication backend [\#175](https://github.com/omab/python-social-auth/issues/175)
- Django usernames more then 30 charracters, via setting variable [\#174](https://github.com/omab/python-social-auth/issues/174)
- Dropbox Lack of Encoding Causes Connection Failures [\#173](https://github.com/omab/python-social-auth/issues/173)
- On new Tumblr login: AttributeError: 'NoneType' object has no attribute 'expiration\_datetime' [\#172](https://github.com/omab/python-social-auth/issues/172)
- Tornado example not working ? [\#171](https://github.com/omab/python-social-auth/issues/171)
- Unicode-object must be encoded before hashing [\#168](https://github.com/omab/python-social-auth/issues/168)
- Accessing access\_token ? [\#167](https://github.com/omab/python-social-auth/issues/167)
- suggestion: please change the username column in auth\_user from "name" to "domain" for weibo backend [\#164](https://github.com/omab/python-social-auth/issues/164)
- Invalid openid.mode: '\<No mode set\>' [\#163](https://github.com/omab/python-social-auth/issues/163)
- get\_user\_id refers to details [\#136](https://github.com/omab/python-social-auth/issues/136)

**Merged pull requests:**

- Add version parameter to foursquare backend [\#176](https://github.com/omab/python-social-auth/pull/176) ([michisu](https://github.com/michisu))
- Added PixelPin to list of providers [\#170](https://github.com/omab/python-social-auth/pull/170) ([lukos](https://github.com/lukos))
- Added new PixelPin provider. [\#169](https://github.com/omab/python-social-auth/pull/169) ([lukos](https://github.com/lukos))
- Serializer changed. [\#165](https://github.com/omab/python-social-auth/pull/165) ([omgbbqhaxx](https://github.com/omgbbqhaxx))

## [v0.1.20](https://github.com/omab/python-social-auth/tree/v0.1.20) (2014-01-17)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.19...v0.1.20)

**Closed issues:**

- docs and examples not included in pypi tarball [\#162](https://github.com/omab/python-social-auth/issues/162)
- Unable to retrieve any extra\_data from LinkedIn backend [\#161](https://github.com/omab/python-social-auth/issues/161)
- Twitter backend error with Python 3.3 [\#139](https://github.com/omab/python-social-auth/issues/139)

## [v0.1.19](https://github.com/omab/python-social-auth/tree/v0.1.19) (2014-01-16)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.18...v0.1.19)

## [v0.1.18](https://github.com/omab/python-social-auth/tree/v0.1.18) (2014-01-16)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.17...v0.1.18)

**Closed issues:**

- GooglePlusAuth backend do not store 'access\_token' on extra\_data \(psa v0.1.17\) [\#157](https://github.com/omab/python-social-auth/issues/157)
- partial pipeline "example.app.pipeline.require\_email" for django does not work [\#152](https://github.com/omab/python-social-auth/issues/152)
- Other dependencies missing [\#151](https://github.com/omab/python-social-auth/issues/151)
- Force https redirect\_uri causes Exception when loading strategy [\#148](https://github.com/omab/python-social-auth/issues/148)
- ValueError: too many values to unpack [\#146](https://github.com/omab/python-social-auth/issues/146)
- AuthCanceled: Authentication process canceled Error [\#144](https://github.com/omab/python-social-auth/issues/144)
- django nonce salt field is too short [\#141](https://github.com/omab/python-social-auth/issues/141)
- Missing dependencies in readme [\#140](https://github.com/omab/python-social-auth/issues/140)
- Incorrect Client Credentials via GitHub [\#138](https://github.com/omab/python-social-auth/issues/138)
- Could I redirect complete page to original login page? [\#137](https://github.com/omab/python-social-auth/issues/137)
- User-friendly backend names [\#132](https://github.com/omab/python-social-auth/issues/132)
- Yahoo backend handle key error [\#125](https://github.com/omab/python-social-auth/issues/125)
- Use constant time comparison function [\#122](https://github.com/omab/python-social-auth/issues/122)
- Inquiry: Why is social.tests.backends not part of the package? [\#119](https://github.com/omab/python-social-auth/issues/119)
- How to get Facebook username during Social authentication [\#117](https://github.com/omab/python-social-auth/issues/117)
- How to get backend instance [\#114](https://github.com/omab/python-social-auth/issues/114)
- Connecting multiple social auths from same provider [\#112](https://github.com/omab/python-social-auth/issues/112)
- Linkedin JSAPI and exchanging Client-side Bearer Token for OAuth 1.0a  token [\#111](https://github.com/omab/python-social-auth/issues/111)
- get\_strategy\(\) got multiple values for keyword argument 'request' [\#110](https://github.com/omab/python-social-auth/issues/110)
- Twitter OAuth ValueError [\#107](https://github.com/omab/python-social-auth/issues/107)
- Facebook scope not set anymore [\#106](https://github.com/omab/python-social-auth/issues/106)
- Namespacing for python-social-auth [\#103](https://github.com/omab/python-social-auth/issues/103)
- Additional backend API calls after user authorization [\#102](https://github.com/omab/python-social-auth/issues/102)
- Linkedin OAuth not working [\#101](https://github.com/omab/python-social-auth/issues/101)
- Make extending SOCIAL\_AUTH\_PIPELINE easier [\#99](https://github.com/omab/python-social-auth/issues/99)
- Authentication problem with Weibo backend when integrate with Django application [\#98](https://github.com/omab/python-social-auth/issues/98)
- Odnoklassniki - PARAM\_API\_KEY : No application key [\#97](https://github.com/omab/python-social-auth/issues/97)
- Per backend FORCE\_EMAIL\_VALIDATION is not respected [\#95](https://github.com/omab/python-social-auth/issues/95)
- Migrating from django\_social\_auth [\#94](https://github.com/omab/python-social-auth/issues/94)
- UnicodeError in mailru backend [\#91](https://github.com/omab/python-social-auth/issues/91)
- setting OPENID\_PAPE\_MAX\_AUTH\_AGE equal to zero doesn't force reauthentication [\#89](https://github.com/omab/python-social-auth/issues/89)
- added associate\_by\_email to pipeline but still adding new account when i login with a social account [\#84](https://github.com/omab/python-social-auth/issues/84)
- LinkedIn OAuth2 bad request. [\#58](https://github.com/omab/python-social-auth/issues/58)

**Merged pull requests:**

- AUTHORIZATION\_URL changed to https [\#160](https://github.com/omab/python-social-auth/pull/160) ([harshiljain](https://github.com/harshiljain))
- GooglePlusAuth backend do not store 'access\_token' on extra\_data \(psa v0.1.17\) [\#159](https://github.com/omab/python-social-auth/pull/159) ([jgsogo](https://github.com/jgsogo))
- Solves some revoke\_token related errors \(BaseOAuth1 and FacebookOAuth2\) [\#158](https://github.com/omab/python-social-auth/pull/158) ([jgsogo](https://github.com/jgsogo))
- odnoklassniki backend iframe app fix [\#156](https://github.com/omab/python-social-auth/pull/156) ([maxtepkeev](https://github.com/maxtepkeev))
- Update Flask integration to most recent version [\#150](https://github.com/omab/python-social-auth/pull/150) ([xen](https://github.com/xen))
- Fixed issue with redirect\_uri with https [\#149](https://github.com/omab/python-social-auth/pull/149) ([roberto-robles](https://github.com/roberto-robles))
- add docs for backend Taobao [\#147](https://github.com/omab/python-social-auth/pull/147) ([jcouyang](https://github.com/jcouyang))
- Add support for \(淘宝\)Taobao OAuth2 [\#145](https://github.com/omab/python-social-auth/pull/145) ([jcouyang](https://github.com/jcouyang))
- Add Dropbox OAuth2 Support [\#143](https://github.com/omab/python-social-auth/pull/143) ([coddingtonbear](https://github.com/coddingtonbear))
- increasing length of salt field for django apps, fixes \#141 [\#142](https://github.com/omab/python-social-auth/pull/142) ([eknuth](https://github.com/eknuth))
- Add support for OpenStreetMap OAuth [\#135](https://github.com/omab/python-social-auth/pull/135) ([Xmypblu](https://github.com/Xmypblu))
- Support for MongoEngine authentication using Custom User Model [\#134](https://github.com/omab/python-social-auth/pull/134) ([ncortot](https://github.com/ncortot))
- Update reddit.py - comment was referencing Github. [\#133](https://github.com/omab/python-social-auth/pull/133) ([gorillamania](https://github.com/gorillamania))
- Tiny typo fix [\#130](https://github.com/omab/python-social-auth/pull/130) ([parlarjb](https://github.com/parlarjb))
- fix session expiration in vk backend [\#129](https://github.com/omab/python-social-auth/pull/129) ([maxtepkeev](https://github.com/maxtepkeev))
- Added support for named URLs and URL translation using the django built-... [\#127](https://github.com/omab/python-social-auth/pull/127) ([hekevintran](https://github.com/hekevintran))
- Updated pipeline example to include externalized auth. [\#126](https://github.com/omab/python-social-auth/pull/126) ([bimsapi](https://github.com/bimsapi))
- Removed non-ascii character from author string [\#123](https://github.com/omab/python-social-auth/pull/123) ([monkut](https://github.com/monkut))
- Add test backends to the package. [\#121](https://github.com/omab/python-social-auth/pull/121) ([hansl](https://github.com/hansl))
- Missing trailing slash on complete url [\#120](https://github.com/omab/python-social-auth/pull/120) ([gorghoa](https://github.com/gorghoa))
- getpocket.com backend [\#116](https://github.com/omab/python-social-auth/pull/116) ([stephenmcd](https://github.com/stephenmcd))
- fix uid in coinbase oauth [\#109](https://github.com/omab/python-social-auth/pull/109) ([FloorLamp](https://github.com/FloorLamp))
- Add Coinbase OAuth2 [\#105](https://github.com/omab/python-social-auth/pull/105) ([FloorLamp](https://github.com/FloorLamp))
- Update weibo.py [\#100](https://github.com/omab/python-social-auth/pull/100) ([josseph](https://github.com/josseph))
- Make vk-app backend to retrieve additional user data in respect to the \*\_EXTRA\_DATA setting [\#96](https://github.com/omab/python-social-auth/pull/96) ([maxtepkeev](https://github.com/maxtepkeev))
- Refresh the docs on http://psa.matiasaguirre.net/docs/ [\#93](https://github.com/omab/python-social-auth/pull/93) ([sahilgupta](https://github.com/sahilgupta))
- Allow for server side flow for Google+ [\#92](https://github.com/omab/python-social-auth/pull/92) ([assiotis](https://github.com/assiotis))
- Fitbit uid [\#90](https://github.com/omab/python-social-auth/pull/90) ([juanriaza](https://github.com/juanriaza))

## [v0.1.17](https://github.com/omab/python-social-auth/tree/v0.1.17) (2013-11-13)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.16...v0.1.17)

**Closed issues:**

- Problem with weibo backend [\#85](https://github.com/omab/python-social-auth/issues/85)
- Steam auth 401 Client Error: Unauthorized [\#82](https://github.com/omab/python-social-auth/issues/82)
- Unit Test Django Client Login? [\#81](https://github.com/omab/python-social-auth/issues/81)
- Facebook profile picture [\#80](https://github.com/omab/python-social-auth/issues/80)
- AttributeError at /user/login/yahoo/ 'Association' object has no attribute 'id' [\#78](https://github.com/omab/python-social-auth/issues/78)
- Extending mongoengine User model for  SOCIAL\_AUTH\_USER\_MODEL [\#70](https://github.com/omab/python-social-auth/issues/70)
- Clarify what the callback url should be for github backend [\#66](https://github.com/omab/python-social-auth/issues/66)
- Duplicate entry error when updating an existing user with a social user [\#63](https://github.com/omab/python-social-auth/issues/63)
- Problem with do\_complete for Facebook backend [\#39](https://github.com/omab/python-social-auth/issues/39)
- Using UserSocialAuth model with Django's generic FKs breaks [\#38](https://github.com/omab/python-social-auth/issues/38)

**Merged pull requests:**

- Use strategy.backend.name instead of strategy.backend\_name [\#88](https://github.com/omab/python-social-auth/pull/88) ([nitishr](https://github.com/nitishr))
- Use strategy.backend.name instead of strategy.backend\_name [\#87](https://github.com/omab/python-social-auth/pull/87) ([nitishr](https://github.com/nitishr))
- Use strategy.backend.name instead of strategy.backend\_name [\#86](https://github.com/omab/python-social-auth/pull/86) ([nitishr](https://github.com/nitishr))
- Raise Http404 in django auth view when the backend is not found [\#83](https://github.com/omab/python-social-auth/pull/83) ([despawnerer](https://github.com/despawnerer))
- Mod: URL for registering Windows Live key/secret [\#79](https://github.com/omab/python-social-auth/pull/79) ([yegle](https://github.com/yegle))

## [v0.1.16](https://github.com/omab/python-social-auth/tree/v0.1.16) (2013-11-07)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.15...v0.1.16)

**Closed issues:**

- TypeError at /auth/login/google/: int\(\) argument must be a string or a number, not Association [\#76](https://github.com/omab/python-social-auth/issues/76)
- Problem with Douban backend [\#72](https://github.com/omab/python-social-auth/issues/72)

**Merged pull requests:**

- Include actions module in distribution [\#77](https://github.com/omab/python-social-auth/pull/77) ([nijel](https://github.com/nijel))
- Update partial from session with more recent values from kwargs [\#75](https://github.com/omab/python-social-auth/pull/75) ([branden](https://github.com/branden))
- Tox support [\#74](https://github.com/omab/python-social-auth/pull/74) ([noirbizarre](https://github.com/noirbizarre))
- quote message for url inclusion in Django middleware [\#73](https://github.com/omab/python-social-auth/pull/73) ([noirbizarre](https://github.com/noirbizarre))
- Return the updated dict. [\#71](https://github.com/omab/python-social-auth/pull/71) ([branden](https://github.com/branden))

## [v0.1.15](https://github.com/omab/python-social-auth/tree/v0.1.15) (2013-11-04)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.14...v0.1.15)

**Closed issues:**

- Complete authentication through REST API [\#68](https://github.com/omab/python-social-auth/issues/68)
- Is there a short way to  connect a social account to existing user [\#62](https://github.com/omab/python-social-auth/issues/62)
- typo in docstring [\#61](https://github.com/omab/python-social-auth/issues/61)
- Latest version tag gone wrong [\#60](https://github.com/omab/python-social-auth/issues/60)
- LinkedIn extra\_data only partially retrieved [\#57](https://github.com/omab/python-social-auth/issues/57)
- Django/Facebook login issue [\#56](https://github.com/omab/python-social-auth/issues/56)
- user\_details pipeline does not update protected fields for new users [\#55](https://github.com/omab/python-social-auth/issues/55)
- Bug in login with Django 1.6 [\#53](https://github.com/omab/python-social-auth/issues/53)
- Token refreshing [\#52](https://github.com/omab/python-social-auth/issues/52)
- Simple question - template use [\#50](https://github.com/omab/python-social-auth/issues/50)
- Django - Error when I try to run ./manage.py [\#48](https://github.com/omab/python-social-auth/issues/48)

**Merged pull requests:**

- Add Tornado Support. [\#69](https://github.com/omab/python-social-auth/pull/69) ([san-mate](https://github.com/san-mate))
- Function user\_data returns list. This leads to exception in social/backe... [\#67](https://github.com/omab/python-social-auth/pull/67) ([akamit](https://github.com/akamit))
- Add RunKeeper [\#65](https://github.com/omab/python-social-auth/pull/65) ([JasonSanford](https://github.com/JasonSanford))
- Make partial\_pipeline JSON serializable for django 1.6 [\#64](https://github.com/omab/python-social-auth/pull/64) ([hannseman](https://github.com/hannseman))
- Appsfuel doc from dsa to psa [\#59](https://github.com/omab/python-social-auth/pull/59) ([z4r](https://github.com/z4r))
- Add openSUSE OpenID login [\#51](https://github.com/omab/python-social-auth/pull/51) ([nijel](https://github.com/nijel))
- `sanitize\_redirect` don't work with Django's `reverse\_lazy` [\#49](https://github.com/omab/python-social-auth/pull/49) ([volrath](https://github.com/volrath))

## [v0.1.14](https://github.com/omab/python-social-auth/tree/v0.1.14) (2013-10-07)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.13...v0.1.14)

**Closed issues:**

- Amazon oauth , client\_id of None in url? [\#47](https://github.com/omab/python-social-auth/issues/47)
- AttributeError: 'str' object has no attribute '\_meta' in Django's admin.py [\#45](https://github.com/omab/python-social-auth/issues/45)
- Invalid documentation for Yahoo OAuth key/secret [\#43](https://github.com/omab/python-social-auth/issues/43)
- using mongoengine \> 0.8, referencefields now store objectids not dbrefs [\#42](https://github.com/omab/python-social-auth/issues/42)
- Google OAuth2 Disconnect [\#41](https://github.com/omab/python-social-auth/issues/41)
- KeyError at /complete/facebook/ when trying to sign in without verifying e-mail address [\#40](https://github.com/omab/python-social-auth/issues/40)
- MongoEngine compability [\#37](https://github.com/omab/python-social-auth/issues/37)
- TypeError at /complete/facebook/ [\#36](https://github.com/omab/python-social-auth/issues/36)

**Merged pull requests:**

- Fixes \#45 -- AttributeError while resolving the user model in Django [\#46](https://github.com/omab/python-social-auth/pull/46) ([MarkusH](https://github.com/MarkusH))
- Add python 3.3 and django 1.6 compatibility [\#44](https://github.com/omab/python-social-auth/pull/44) ([nvbn](https://github.com/nvbn))

## [v0.1.13](https://github.com/omab/python-social-auth/tree/v0.1.13) (2013-09-22)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.12...v0.1.13)

**Closed issues:**

- Error: django.db.models.fields.subclassing.JSONField [\#35](https://github.com/omab/python-social-auth/issues/35)
- some linkedin oauth2 extra data doesn't show up [\#34](https://github.com/omab/python-social-auth/issues/34)
- Odnoklassniki backend requires authization by POST [\#33](https://github.com/omab/python-social-auth/issues/33)
- SOCIAL\_AUTH\_GOOGLE\_OAUTH2\_EXTRA\_SCOPE is ignored [\#28](https://github.com/omab/python-social-auth/issues/28)
- Example for pyramid [\#27](https://github.com/omab/python-social-auth/issues/27)
- Not working with instagram api [\#21](https://github.com/omab/python-social-auth/issues/21)

**Merged pull requests:**

- Update README.rst [\#32](https://github.com/omab/python-social-auth/pull/32) ([jontsai](https://github.com/jontsai))
- Update pipeline.rst [\#31](https://github.com/omab/python-social-auth/pull/31) ([jontsai](https://github.com/jontsai))
- Update README.rst [\#30](https://github.com/omab/python-social-auth/pull/30) ([jontsai](https://github.com/jontsai))

## [v0.1.12](https://github.com/omab/python-social-auth/tree/v0.1.12) (2013-09-13)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.11...v0.1.12)

**Closed issues:**

- Setting the facebook scope wrongly documented [\#29](https://github.com/omab/python-social-auth/issues/29)

**Merged pull requests:**

- Fixed auth redirect URL for BaseOauth2 always redirecting wrong [\#26](https://github.com/omab/python-social-auth/pull/26) ([romanalexander](https://github.com/romanalexander))
- Adding support for ThisIsMyJam [\#25](https://github.com/omab/python-social-auth/pull/25) ([systemizer](https://github.com/systemizer))
- Add support for box.net [\#24](https://github.com/omab/python-social-auth/pull/24) ([samkuehn](https://github.com/samkuehn))

## [v0.1.11](https://github.com/omab/python-social-auth/tree/v0.1.11) (2013-09-04)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.10...v0.1.11)

**Closed issues:**

- Steam user ID broken in Django backend [\#23](https://github.com/omab/python-social-auth/issues/23)
- Flask example fails to complete connection to Github [\#22](https://github.com/omab/python-social-auth/issues/22)

## [v0.1.10](https://github.com/omab/python-social-auth/tree/v0.1.10) (2013-08-29)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.9...v0.1.10)

## [v0.1.9](https://github.com/omab/python-social-auth/tree/v0.1.9) (2013-08-29)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.8...v0.1.9)

**Closed issues:**

- google oauth 2.0 [\#20](https://github.com/omab/python-social-auth/issues/20)
- Support for linkedin oauth2 [\#19](https://github.com/omab/python-social-auth/issues/19)
- Invalid Steam backend user id. [\#17](https://github.com/omab/python-social-auth/issues/17)

**Merged pull requests:**

- SQLAlchemy fixes [\#18](https://github.com/omab/python-social-auth/pull/18) ([Flyflo](https://github.com/Flyflo))

## [v0.1.8](https://github.com/omab/python-social-auth/tree/v0.1.8) (2013-07-13)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.7...v0.1.8)

**Merged pull requests:**

- Fix OpenId auth with Flask 0.10 [\#16](https://github.com/omab/python-social-auth/pull/16) ([Flyflo](https://github.com/Flyflo))
- Add CodersClan button [\#13](https://github.com/omab/python-social-auth/pull/13) ([DrorCohenCC](https://github.com/DrorCohenCC))
- Added a default to response in FacebookOAuth.do\_auth [\#12](https://github.com/omab/python-social-auth/pull/12) ([san-mate](https://github.com/san-mate))
- Bug fix of FacebookAppOAuth2 [\#11](https://github.com/omab/python-social-auth/pull/11) ([san-mate](https://github.com/san-mate))

## [v0.1.7](https://github.com/omab/python-social-auth/tree/v0.1.7) (2013-06-03)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.6...v0.1.7)

## [v0.1.6](https://github.com/omab/python-social-auth/tree/v0.1.6) (2013-06-03)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.5...v0.1.6)

## [v0.1.5](https://github.com/omab/python-social-auth/tree/v0.1.5) (2013-06-01)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.4...v0.1.5)

## [v0.1.4](https://github.com/omab/python-social-auth/tree/v0.1.4) (2013-05-31)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.3...v0.1.4)

## [v0.1.3](https://github.com/omab/python-social-auth/tree/v0.1.3) (2013-05-31)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.2...v0.1.3)

**Closed issues:**

- get\_user\_details\(\) vs user\_data\(\) [\#7](https://github.com/omab/python-social-auth/issues/7)

**Merged pull requests:**

- Added support for django custom user with no 'username' field [\#10](https://github.com/omab/python-social-auth/pull/10) ([jgsogo](https://github.com/jgsogo))
- Add Trello backend support [\#9](https://github.com/omab/python-social-auth/pull/9) ([dongweiming](https://github.com/dongweiming))
- Podio backend [\#8](https://github.com/omab/python-social-auth/pull/8) ([gsakkis](https://github.com/gsakkis))
- VK.com \(former vkontakte\) backend update [\#6](https://github.com/omab/python-social-auth/pull/6) ([uruz](https://github.com/uruz))
- Bug fix with Vkontakte provider [\#5](https://github.com/omab/python-social-auth/pull/5) ([kazarinov](https://github.com/kazarinov))

## [v0.1.2](https://github.com/omab/python-social-auth/tree/v0.1.2) (2013-04-04)
[Full Changelog](https://github.com/omab/python-social-auth/compare/v0.1.1...v0.1.2)

**Closed issues:**

- Flask example - missing relation 'social\_auth\_usersocialauth' [\#4](https://github.com/omab/python-social-auth/issues/4)

## [v0.1.1](https://github.com/omab/python-social-auth/tree/v0.1.1) (2013-04-01)
**Closed issues:**

- confusing update to globals in the flask integration [\#1](https://github.com/omab/python-social-auth/issues/1)

**Merged pull requests:**

- Fixed South introspection path to new module structure. [\#2](https://github.com/omab/python-social-auth/pull/2) ([jezdez](https://github.com/jezdez))



\* *This Change Log was automatically generated by [github_changelog_generator](https://github.com/skywinder/Github-Changelog-Generator)*
