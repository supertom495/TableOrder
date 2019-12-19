import pusher
pusher_client = pusher.Pusher(app_id='12345', key='ABCDEF', secret='HIJKLMNOP', ssl=False, host='192.168.1.26', port=6001)

pusher_client.trigger(u'posts.10', u'AddDish', {u'some': u'data'})
