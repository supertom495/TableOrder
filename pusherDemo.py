import pusher
pusher_client = pusher.Pusher(app_id=u'623887', key=u'd422ef617a70042aa6b2', secret=u'41e0bf31ef4a3b19b849', cluster=u'ap1')

pusher_client.trigger(u'posts.10', u'AddDish', {u'some': u'data'})
