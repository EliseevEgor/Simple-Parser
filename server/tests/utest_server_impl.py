import unittest

from fastapi import HTTPException

import main
from server.main import server_impl
from server.utils.constants import ROOT_MESSAGE, EXCEPTION_HTTPError_TEXT
from fastapi.testclient import TestClient
import server.main.server_impl as server

client = TestClient(server.app)
server.init(main.get_dir())


class RequestUtilsTest(unittest.TestCase):

    def test_root(self):
        res = client.get("/root")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), ROOT_MESSAGE)

    def test_root_err(self):
        res = client.get("/root/1")
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json(), {"detail": "Not Found"})

    def save_info(self):
        res = client.post("/companies/",
                          json={
                              "name": "myComp",
                              "symbol": "AM",
                              "fields": []
                          })
        try:
            server_impl.request_func.DB.get("myComp")
        except KeyError:
            self.fail("Test failed")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {
            "name": "myComp",
            "symbol": "AM",
            "fields": []
        })

    def test_save_info_about_company(self):
        self.save_info()
        server_impl.request_func.DB.clear()

    def test_get_info(self):
        try:
            res = client.get("v1/AM/summary/")
            self.assertEqual(res.status_code, 200)
            json = res.json()
            self.assertIsNotNone(json.get('price'))
            self.assertIsNotNone(json.get('open'))
            self.assertIsNotNone(json.get('prev_close'))
        except Exception:
            self.fail("Test failed")

    def test_get_info_exc(self):
        res = client.get("v1/abcde/summary/")
        self.assertEqual(res.status_code, 500)
        self.assertEqual(res.json(), {'detail': EXCEPTION_HTTPError_TEXT})

    def test_delete_company_ex(self):
        res = client.delete("/companies/",
                            json={
                                "name": "myComp",
                                "symbol": "AM",
                                "fields": []
                            })
        self.assertEqual(res.status_code, 404)
        self.assertEqual(server_impl.request_func.DB.size(), 0)

    def test_delete_company(self):
        self.save_info()
        try:
            client.delete("/companies/",
                          json={
                              "name": "myComp",
                              "symbol": "AM",
                              "fields": []
                          })
        except HTTPException:
            self.fail("test failed")

        with self.assertRaises(KeyError):
            server_impl.request_func.DB.get("myComp")

        self.assertEqual(server_impl.request_func.DB.size(), 0)


if __name__ == '__main__':
    unittest.main()
