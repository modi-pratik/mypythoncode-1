__author__ = 'stonex'

import xmpp

username = 'snehalpp'
passwd = 'snehal'
to = 'test_user@192.168.4.86'
msg = 'hello :)'
jid = xmpp.JID('snehalpp@192.168.4.86')
# jid = 8573862411423635391726198
cl = xmpp.Client(jid.getDomain(), debug=[])
cl.connect()
cl.auth(user=username, password=passwd)
cl.auth(jid.getNode(), passwd)
# import ipdb
# ipdb.set_trace()
cl.sendInitPresence()
cl.send(xmpp.protocol.Message(to, msg))


# client = xmpp.Client('192.168.4.86')
# client.connect(server=('192.168.4.86', 5280))
# client.auth(username, passwd, 'botty')
# client.sendInitPresence()
# message = xmpp.Message(to, msg)
# message.setAttr('type', 'chat')
# client.send(message)
