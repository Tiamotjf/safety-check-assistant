import http.cookiejar
import json
import threading
import unittest
import urllib.request
import urllib.error
from http.server import ThreadingHTTPServer
from app import Handler, SESSIONS

class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(("127.0.0.1",0),Handler)
        cls.base=f"http://127.0.0.1:{cls.server.server_port}"
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
    @classmethod
    def tearDownClass(cls):cls.server.shutdown();cls.server.server_close()
    def client(self):return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def request(self,c,path,data=None,origin=None):
        headers={"Content-Type":"application/json","X-Local-Review":"1"}
        if origin:headers["Origin"]=origin
        req=urllib.request.Request(self.base+path,data=json.dumps(data).encode() if data is not None else None,headers=headers)
        with c.open(req) as r:return json.load(r)
    def test_browser_sessions_are_separate(self):
        a,b=self.client(),self.client();self.request(a,"/api/state");self.request(b,"/api/state")
        self.request(a,"/api/scenario",{"scenario":"risk"})
        self.assertEqual(self.request(b,"/api/state")["scenario"],"normal")
    def test_cross_origin_post_rejected(self):
        with self.assertRaises(urllib.error.HTTPError) as e:self.request(self.client(),"/api/prepare",{},"http://other.example")
        self.assertEqual(e.exception.code,403)
    def test_api_normal_flow(self):
        c=self.client();self.request(c,"/api/state");s=self.request(c,"/api/prepare",{})
        token=self.request(c,"/api/review",{"revision":s["revision"],"checked":True})["token"]
        self.assertEqual(self.request(c,"/api/send",{"token":token})["stage"],"sent")
    def test_api_validation_cannot_bypass_gate(self):
        c=self.client();self.request(c,"/api/scenario",{"scenario":"risk"});s=self.request(c,"/api/prepare",{})
        with self.assertRaises(urllib.error.HTTPError) as e:self.request(c,"/api/review",{"revision":s["revision"],"checked":True})
        self.assertEqual(e.exception.code,400)

if __name__=="__main__":unittest.main()
