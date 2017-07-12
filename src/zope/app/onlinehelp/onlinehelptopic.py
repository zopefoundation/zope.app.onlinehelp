##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Implementation of an Online Help Topic.

"""
from __future__ import absolute_import
__docformat__ = 'restructuredtext'

import os

from persistent import Persistent
from zope.interface import implementer
from zope.configuration.exceptions import ConfigurationError
from zope.contenttype import guess_content_type

from zope.container.sample import SampleContainer
from zope.app.file.image import getImageInfo

from zope.app.onlinehelp.interfaces import IOnlineHelpTopic
from zope.app.onlinehelp.interfaces import ISourceTextOnlineHelpTopic
from zope.app.onlinehelp.interfaces import IRESTOnlineHelpTopic
from zope.app.onlinehelp.interfaces import ISTXOnlineHelpTopic
from zope.app.onlinehelp.interfaces import IZPTOnlineHelpTopic
from zope.app.onlinehelp.interfaces import IOnlineHelpResource


DEFAULT_ENCODING = "utf-8"

try:
    text_type = unicode
except NameError:
    text_type = str

@implementer(IOnlineHelpResource)
class OnlineHelpResource(Persistent):
    r"""
    Represents a resource that is used inside
    the rendered Help Topic - for example a screenshot.

    Implements :class:`~zope.app.onlinehelp.interfaces.IOnlineHelpResource`.

    >>> from zope.app.onlinehelp.tests.test_onlinehelp import testdir
    >>> path = os.path.join(testdir(), 'test1.png')

    >>> resource = OnlineHelpResource(path)
    >>> resource.contentType
    'image/png'
    >>> resource._fileMode
    'rb'

    >>> path = os.path.join(testdir(), 'help2.txt')

    >>> resource = OnlineHelpResource(path)
    >>> resource.contentType
    'text/plain'
    >>> resource._fileMode
    'r'
    >>> resource.data.splitlines()[0]
    u'This is another help!'
    >>> u'\u0444\u0430\u0439\u043b' in resource.data
    True
    """

    def __init__(self, path='', contentType=''):
        self.path = path
        with open(os.path.normpath(self.path), 'rb') as f:
            _data = f.read()
        self._size = len(_data)
        self._fileMode = 'rb'
        encoding = None

        if contentType == '':
            content_type, encoding = guess_content_type(self.path, _data, '')

        if content_type.startswith('image/'):
            self.contentType, _width, _height = getImageInfo(_data)
        else:
            self.contentType = content_type

        self._encoding = encoding or DEFAULT_ENCODING
        if self.contentType.startswith('text/'):
            self._fileMode = 'r'

    @property
    def data(self):
        with open(os.path.normpath(self.path), self._fileMode) as f:
            data = f.read()
        if self.contentType.startswith('text/') and not isinstance(data, text_type):
            data = data.decode(self._encoding)
        return data

    def getSize(self):
        '''See IFile'''
        return self._size


class BaseOnlineHelpTopic(SampleContainer):
    """Base class for custom Help Topic implementations.

      >>> from zope.app.onlinehelp.tests.test_onlinehelp import testdir
      >>> path = os.path.join(testdir(), 'help.txt')

    Create a Help Topic from a file

      >>> topic = BaseOnlineHelpTopic('help','Help',path,'')

    Test the title

      >>> topic.title
      'Help'

    Test the topic path

      >>> topic.getTopicPath()
      'help'
      >>> topic.parentPath = 'parent'
      >>> topic.getTopicPath()
      'parent/help'

    Resources can be added to an online help topic.

      >>> topic.addResources(['test1.png', 'test2.png'])
      >>> topic['test1.png'].contentType
      'image/png'
      >>> topic['test2.png'].contentType
      'image/png'
    """

    id = u""
    title = u""
    path = u""
    parentPath = u""
    interface = None
    view = None

    def __init__(self, id, title, path, parentPath, interface=None, view=None):
        """Initialize object."""
        self.id = id
        self.parentPath = parentPath
        self.title = title
        self.path = path
        self.interface = interface
        self.view = view

        if not os.path.exists(self.path):
            raise ConfigurationError(
                "Help Topic definition %s does not exist" % self.path
                )

        super(BaseOnlineHelpTopic, self).__init__()

    def _newContainerData(self):
        # Ensure consistent iteration order for tests.
        from collections import OrderedDict
        return OrderedDict()

    def addResources(self, resources):
        """ see IOnlineHelpTopic """
        dirname = os.path.dirname(self.path)
        for resource in resources:
            resource_path = dirname + '/' + resource
            if os.path.exists(resource_path):
                self[resource] = OnlineHelpResource(resource_path)

    def getTopicPath(self):
        """See IOnlineHelpTopic"""
        if self.parentPath:
            return self.parentPath + '/' + self.id
        return self.id

    def getSubTopics(self):
        res = []
        for item in self.values():
            if IOnlineHelpTopic.providedBy(item):
                res.append(item)

        return res


class SourceTextOnlineHelpTopic(BaseOnlineHelpTopic):
    """Source text methods mixin class."""

    type = None

    @property
    def source(self):
        with open(os.path.normpath(self.path), 'rb') as f:
            source = f.read()
        return source.decode(DEFAULT_ENCODING)


@implementer(ISourceTextOnlineHelpTopic)
class OnlineHelpTopic(SourceTextOnlineHelpTopic):
    """
    Represents a Help Topic. This generic implementation uses the filename
    extension for guess the type. This topic implementation supports plain
    text topics, restructured and structured text topics. HTML topics get
    rendered as structured text. If a file doesn't have the right file
    extension, use a explicit topic class for representing the right format.

    Implements :class:`~zope.app.onlinehelp.interfaces.ISourceTextOnlineHelpTopic`.

      >>> from zope.app.onlinehelp.tests.test_onlinehelp import testdir
      >>> path = os.path.join(testdir(), 'help.txt')

    Create a Help Topic from a file

      >>> topic = OnlineHelpTopic('help','Help',path,'')

    Test the title

      >>> topic.title
      'Help'

    Test the topic path

      >>> topic.getTopicPath()
      'help'
      >>> topic.parentPath = 'parent'
      >>> topic.getTopicPath()
      'parent/help'

    The type should be set to plaintext, since
    the file extension is 'txt'

      >>> topic.type
      'zope.source.plaintext'

    Test the help content.

      >>> topic.source
      u'This is a help!'

      >>> path = os.path.join(testdir(), 'help.stx')
      >>> topic = OnlineHelpTopic('help','Help',path,'')

    The type should now be structured text

      >>> topic.type
      'zope.source.stx'

    HTML files are treated as structured text files

      >>> path = os.path.join(testdir(), 'help.html')
      >>> topic = OnlineHelpTopic('help','Help',path,'')

    The type should still be structured text

      >>> topic.type
      'zope.source.stx'

      >>> path = os.path.join(testdir(), 'help.rst')
      >>> topic = OnlineHelpTopic('help','Help',path,'')

    The type should now be restructured text

      >>> topic.type
      'zope.source.rest'

    Resources can be added to an online help topic.

      >>> topic.addResources(['test1.png', 'test2.png'])
      >>> topic['test1.png'].contentType
      'image/png'
      >>> topic['test2.png'].contentType
      'image/png'
    """

    def __init__(self, id, title, path, parentPath, interface=None, view=None):
        """Initialize object."""
        super(OnlineHelpTopic, self).__init__(id, title, path, parentPath,
              interface, view)

        filename = os.path.basename(path.lower())
        file_ext = 'txt'
        if len(filename.split('.'))>1:
            file_ext = filename.split('.')[-1]

        self.type = 'zope.source.plaintext'

        if file_ext in ('rst', 'rest') :
            self.type = 'zope.source.rest'
        elif file_ext in ('stx', 'html', 'htm'):
            self.type = 'zope.source.stx'


@implementer(IRESTOnlineHelpTopic)
class RESTOnlineHelpTopic(SourceTextOnlineHelpTopic):
    r"""
    Represents a restructed text based Help Topic which has other
    filename extension then '.rst' or 'rest'.

    Implements :class:`~zope.app.onlinehelp.interfaces.IRESTOnlineHelpTopic`.

      >>> from zope.app.onlinehelp.tests.test_onlinehelp import testdir
      >>> path = os.path.join(testdir(), 'help.rst')

    Create a Help Topic from a file

      >>> topic = RESTOnlineHelpTopic('help','Help',path,'')

    Test the title

      >>> topic.title
      'Help'

    Test the topic path

      >>> topic.getTopicPath()
      'help'
      >>> topic.parentPath = 'parent'
      >>> topic.getTopicPath()
      'parent/help'

    The type should be set to rest, since the file extension is 'rest'

      >>> topic.type
      'zope.source.rest'

    Test the help content.

      >>> topic.source.splitlines()[0]
      u'This is a ReST help!'
      >>> u'\u0444\u0430\u0439\u043b' in topic.source
      True

    Resources can be added to an online help topic.

      >>> topic.addResources(['test1.png', 'test2.png'])
      >>> topic['test1.png'].contentType
      'image/png'
      >>> topic['test2.png'].contentType
      'image/png'
    """

    type = 'zope.source.rest'


@implementer(ISTXOnlineHelpTopic)
class STXOnlineHelpTopic(SourceTextOnlineHelpTopic):
    r"""
    Represents a restructed text based Help Topic which has other
    filename extension then '.stx'.

    Implements :class:`~zope.app.onlinehelp.interfaces.ISTXOnlineHelpTopic`.

      >>> from zope.app.onlinehelp.tests.test_onlinehelp import testdir
      >>> path = os.path.join(testdir(), 'help.stx')

    Create a Help Topic from a file

      >>> topic = STXOnlineHelpTopic('help','Help',path,'')

    Test the title

      >>> topic.title
      'Help'

    Test the topic path

      >>> topic.getTopicPath()
      'help'
      >>> topic.parentPath = 'parent'
      >>> topic.getTopicPath()
      'parent/help'

    The type should be set to stx, since the file extension is 'stx'

      >>> topic.type
      'zope.source.stx'

    Test the help content.

      >>> topic.source.splitlines()[0]
      u'This is a STX help!'
      >>> u'\u0444\u0430\u0439\u043b' in topic.source
      True

    Resources can be added to an online help topic.

      >>> topic.addResources(['test1.png', 'test2.png'])
      >>> topic['test1.png'].contentType
      'image/png'
      >>> topic['test2.png'].contentType
      'image/png'
    """

    type = 'zope.source.stx'

@implementer(IZPTOnlineHelpTopic)
class ZPTOnlineHelpTopic(BaseOnlineHelpTopic):
    r"""Represents a page template based Help Topic which has other
    filename extension than `.pt`.

    Implements :class:`~zope.app.onlinehelp.interfaces.IZPTOnlineHelpTopic`.

      >>> from zope.publisher.browser import TestRequest, BrowserView
      >>> from zope.app.pagetemplate.viewpagetemplatefile import \
      ...     ViewPageTemplateFile
      >>> from zope.app.onlinehelp.tests.test_onlinehelp import testdir
      >>> path = os.path.join(testdir(), 'help.pt')

    Create a page template based Help Topic from a file

      >>> topic = ZPTOnlineHelpTopic('help','Help',path,'')

    Test the title

      >>> topic.title
      'Help'

    Test the topic path

      >>> topic.getTopicPath()
      'help'
      >>> topic.parentPath = 'parent'
      >>> topic.getTopicPath()
      'parent/help'

    Test the help content.

      >>> class TestView(BrowserView):
      ...     def index(self):
      ...         path = self.context.path
      ...         view = ViewPageTemplateFile(path)
      ...         return view(self)
      >>> request = TestRequest()
      >>> view = TestView(topic, request)
      >>> res = view.index()
      >>> u'<span>This is a ZPT help!</span>' in res
      True
      >>> u'\u0444\u0430\u0439\u043b' in res
      True

    Resources can be added to an online help topic.

      >>> topic.addResources(['test1.png', 'test2.png'])
      >>> topic['test1.png'].contentType
      'image/png'
      >>> topic['test2.png'].contentType
      'image/png'
    """
