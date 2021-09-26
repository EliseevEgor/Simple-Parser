import unittest

import main
import json
from server.utils.constants import (
    URL,
    ROOT_MESSAGE, CONFIG_PATH
)
from fastapi import HTTPException
from server.main.request_utils import RequestsUtils


def init_elems():
    with open(main.get_dir() + CONFIG_PATH, 'r+') as f:
        data = f.read()
    return json.loads(data)


utils = RequestsUtils(URL, init_elems())


class RequestUtilsTest(unittest.TestCase):
    def helper_save_company(self, name, info):
        utils.save_company(name, info)

        self.assertTrue(utils.DB.get(name) is not None)
        self.assertEqual(utils.DB.get(name), info)

    def helper_delete_company(self, name):
        utils.del_company(name)
        self.assertEqual(utils.DB.size(), 0)
        with self.assertRaises(KeyError):
            utils.DB.get(name)

    def test_root_func(self):
        res = utils.root_func()
        self.assertEqual(res, ROOT_MESSAGE)

    def test_get_info_raise_exception(self):
        with self.assertRaises(HTTPException):
            utils.get_info_about_company("lksadjfkldj", None)

    def test_get_info_ok(self):
        try:
            utils.get_info_about_company("AM", None)
        except Exception:
            self.fail("Test failed")

    def test_save_company(self):
        self.helper_save_company("My_company", "my_info")
        utils.DB.delete("My_company")

    def test_delete_company(self):
        self.helper_save_company("My_company", "my_info")
        self.helper_delete_company("My_company")


if __name__ == '__main__':
    unittest.main()
