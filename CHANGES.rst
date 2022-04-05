=========
 CHANGES
=========

4.2.0 (2022-04-05)
==================

- Add support for Python 3.7, 3.8, 3.9, and 3.10.

- Drop support for Python 3.4.


4.1.0 (2017-07-12)
==================

- The help namespace no longer modifies the global help object on
  traversal. Instead it returns a new proxy object. This makes it
  thread-safe. See `issue 4
  <https://github.com/zopefoundation/zope.app.onlinehelp/issues/4>`_.

- ``getTopicFor`` now really returns the first found topic in the
  event that the object implements multiple interfaces that have
  registered topics for the given view. Previously it would return the
  topic for the least-specific interface.

4.0.1 (2017-05-21)
==================

- Drop test dependency on ``zope.app.securitypolicy``. It wasn't used,
  and it isn't yet fully ported to Python 3.


4.0.0 (2017-05-17)
==================

- Add support for Python 3.4, 3.5, 3.6 and PyPy.

- Change ZODB dependency to persistent.

- Drop test dependency on ``zope.app.testing``,
  ``zope.app.zcmlifiles`` and ``zope.app.apidoc``, among others.

3.5.2 (2010-01-08)
==================

- Fix tests using a newer zope.publisher that requires zope.login.

3.5.1 (2009-03-21)
==================

- Use ``zope.site`` instead of ``zope.app.folder``.

3.5.0 (2009-02-01)
==================

- Removed ``OnlineHelpTopicFactory``, ``simple`` and
  ``SimpleViewClass``. All of them where using old deprecated and
  removed Zope3 imports. None of them where used and tested.

- Use ``zope.container`` instead of ``zope.app.container``.

- Removed use of ``zope.app.zapi``.

3.4.1 (2007-10-25)
==================

- Package meta-data update.


3.4.0 (2007-10-23)
==================

- Initial release independent of the main Zope tree.

Older
=====


Make the onlinehelp utility more component oriented.

- Use registred page/view instead of ViewPageTemplate for rendering topic tree
  This way we can use/register own templates for tree layout.

- Add page template based topic for rendering topics which has to
  call other zope3 resources like javascripts and css styles sheets etc.
  This resources can be rendered in the header area of the onlinehelp_macros.

- Enhance the API of topics and simplyfie the view part.

- Implemented getSubTopics() method on topics. This way we can sublist topics.

- Remove unused onlinehelp code in rotterdam template.pt

- Add type to directive, this supports registration of README.txt as 'rest' topics
