import unittest

from DB.companies import database

USER_ID_1 = 1
USER_ID_2 = 2
USER_ID_3 = 3
COMPANY_NAME_1 = "COMPANY1"
COMPANY_NAME_2 = "COMPANY2"
COMPANY_NAME_3 = "COMPANY3"
COMPANY_NAME_4 = "COMPANY4"
COMPANY_NAME_5 = "COMPANY5"


def helper_SC(id_user):
    return database.get_companies(id_user, "TEST")


def helper_DC(id_user, name):
    return database.delete_company(id_user, name, "TEST")


def helper_AC(id_user, name):
    return database.add_company(id_user, name, "TEST")


def create():
    database.create_table("TEST")


class DBTest(unittest.TestCase):

    def test_one_user(self, id_user=USER_ID_1):
        create()
        self.assertEqual(helper_SC(id_user), "у вас пока что нет изранных компаний")
        ans = helper_AC(id_user, COMPANY_NAME_1)
        self.assertEqual(ans, "Компания {} добавлена".format(COMPANY_NAME_1))
        ans = helper_AC(id_user, COMPANY_NAME_2)
        self.assertEqual(ans, "Компания {} добавлена".format(COMPANY_NAME_2))
        ans = helper_AC(id_user, COMPANY_NAME_3)
        self.assertEqual(ans, "Компания {} добавлена".format(COMPANY_NAME_3))
        ans = helper_AC(id_user, COMPANY_NAME_4)
        self.assertEqual(ans, "Компания {} добавлена".format(COMPANY_NAME_4))
        ans = helper_AC(id_user, COMPANY_NAME_5)
        self.assertEqual(ans, "Компания {} добавлена".format(COMPANY_NAME_5))

        self.assertEqual(helper_SC(id_user), "Ваши компании: \n" +
                         COMPANY_NAME_1 + ",\n" +
                         COMPANY_NAME_2 + ",\n" +
                         COMPANY_NAME_3 + ",\n" +
                         COMPANY_NAME_4 + ",\n" +
                         COMPANY_NAME_5)

        ans = helper_DC(id_user, COMPANY_NAME_5)
        self.assertEqual(ans, "Компания {} удалена".format(COMPANY_NAME_5))
        self.assertEqual(helper_SC(id_user), "Ваши компании: \n" +
                         COMPANY_NAME_1 + ",\n" +
                         COMPANY_NAME_2 + ",\n" +
                         COMPANY_NAME_3 + ",\n" +
                         COMPANY_NAME_4)
        ans = helper_DC(id_user, COMPANY_NAME_4)
        self.assertEqual(ans, "Компания {} удалена".format(COMPANY_NAME_4))
        self.assertEqual(helper_SC(id_user), "Ваши компании: \n" +
                         COMPANY_NAME_1 + ",\n" +
                         COMPANY_NAME_2 + ",\n" +
                         COMPANY_NAME_3)
        ans = helper_DC(id_user, COMPANY_NAME_4)
        self.assertEqual(ans, "Компания {} удалена".format(COMPANY_NAME_4))
        self.assertEqual(helper_SC(id_user), "Ваши компании: \n" +
                         COMPANY_NAME_1 + ",\n" +
                         COMPANY_NAME_2 + ",\n" +
                         COMPANY_NAME_3)
        ans = helper_DC(id_user, COMPANY_NAME_3)
        self.assertEqual(ans, "Компания {} удалена".format(COMPANY_NAME_3))
        self.assertEqual(helper_SC(id_user), "Ваши компании: \n" +
                         COMPANY_NAME_1 + ",\n" +
                         COMPANY_NAME_2)
        ans = helper_DC(id_user, COMPANY_NAME_2)
        self.assertEqual(ans, "Компания {} удалена".format(COMPANY_NAME_2))
        self.assertEqual(helper_SC(id_user), "Ваши компании: \n" +
                         COMPANY_NAME_1)
        ans = helper_DC(id_user, COMPANY_NAME_1)
        self.assertEqual(ans, "Компания {} удалена".format(COMPANY_NAME_1))
        self.assertEqual(helper_SC(id_user), "у вас пока что нет изранных компаний")
        database.drop_table("TEST")

    def test_several_users(self):
        create()
        for user in [USER_ID_1, USER_ID_2, USER_ID_3]:
            self.test_one_user(user)
        database.drop_table("TEST")

    def test_raise_exception(self):
        create()
        u = USER_ID_1
        c = COMPANY_NAME_1

        ans = helper_AC(u, c)
        self.assertEqual(ans, "Компания {} добавлена".format(c))
        ans = helper_AC(u, c)
        self.assertEqual(ans, "Такая компания уже есть")

        ans = helper_DC(u, c)
        self.assertEqual(ans, "Компания {} удалена".format(c))
        database.drop_table("TEST")


if __name__ == '__main__':
    unittest.main()
