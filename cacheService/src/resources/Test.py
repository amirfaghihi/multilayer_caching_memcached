from flask_restful import Resource
import threading


class Test(Resource):
    def __init__(self, mcache):
        self.mcache = mcache

    def get(self):
        th = threading.Thread(target=self.mcache.dummy_wait, args=[10])
        th.start()
        return {"message": "Accepted"}, 202
