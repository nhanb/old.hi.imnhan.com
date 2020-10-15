Title: Random notes
Slug: notes
Hidden: True


In which I jot down scattered tidbits on various topics.

## SRE

There's a good [checklist](http://rachelbythebay.com/w/2019/07/21/reliability/)
on Rachel By The Bay, the gist is:

- Rollbacks should work. On every deployment.

- A to AB to B (a.k.a. make before break):
    + v2 code/data should not break v1 code/data

- Strict(er than JSON) schema-ing when you fling data across places
    + Protobuf, etc.
    + You should only _begin_ to consider JSON if you need to talk to browsers

- Please fix 500s.
    + Also you should only get 400s when talking to external things out of your control

Her [follow-up](http://rachelbythebay.com/w/2019/10/05/nxdomain/) is a nice
scary story too. Also reminder that "infra-as-code" abstractions isn't an
excuse _not_ to learn the underlying infra properly.
