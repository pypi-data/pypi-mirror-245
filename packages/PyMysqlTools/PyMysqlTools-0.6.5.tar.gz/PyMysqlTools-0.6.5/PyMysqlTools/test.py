import PyMysqlTools.main
from PyMysqlTools.settings import DEFAULT_RESULT_SET_TYPE

if __name__ == '__main__':
    mysql = PyMysqlTools.main.Connect(
        database='db_transportation',
        username='root',
        password='123456'
    )

    # mysql.insert_one('tb_account', {
    #     'system': '123',
    #     'system_code': '123',
    #     'username': '123',
    #     'password': '123',
    # })

    # mysql.delete_by_id('tb_account', 7)

    # print(mysql.find_all('tb_account'))

    # print(mysql.show_auto_increment('tb_account'))
    # mysql.reconnect()
    # print(mysql.set_auto_increment('tb_account', 50))

    # print(mysql.show_table_desc('tb_account'))
    print(mysql.show_auto_increment('tb_account'))

    """
    if __name__ == '__main__':
    mysql = Connect(
        **{'user': 'root', 'password': '123456', 'database': 'db_transportation'},
    )
    print(mysql.show_databases())
    """
