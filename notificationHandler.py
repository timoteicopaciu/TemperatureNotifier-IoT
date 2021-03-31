from listener import Listener
from pushbullet import Pushbullet
from threading import Thread

HTTP_PROXY_HOST = None
HTTP_PROXY_PORT = None


class NotificationHandler:
    def __init__(self, pushBulletAPIKey, didReceiveCommand):
        # Setup pushBullet manager
        self.pushBulletAPIKey = pushBulletAPIKey
        self.didReceiveCommand = didReceiveCommand
        self.pushBulletManager = Pushbullet(self.pushBulletAPIKey)
        thread = Thread(target=self.__createListener)
        thread.start()

    def __createListener(self):
        self.listener = Listener(account=self.pushBulletManager, on_push=self.on_push, http_proxy_host=HTTP_PROXY_HOST,
                                 http_proxy_port=HTTP_PROXY_PORT)
        self.listener.run_forever()

    def pushToMobile(self, dataDictionary):
        print("pushToMobile: ", dataDictionary)
        push = self.pushBulletManager.push_note(dataDictionary['text'], '')
        print("push result: ", push)

    def __delete(self):
        self.listener.close()  # to stop the run_forever()

    def on_push(self, jsonMessage):
        if jsonMessage["type"] == "tickle" and jsonMessage["subtype"] == "push":
            allPushes = self.pushBulletManager.get_pushes()
            latest = allPushes[0]
            if 'body' in latest:
                body = latest['body']
                print(body)
                if body.startswith("@"):
                    self.didReceiveCommand(body)
