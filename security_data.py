#coding=utf-8
'''
database of security project
'''
import pymysql


class DatabaseModel():
    def __init__(self, host='localhost', port=3306, user=None, password=None, database=None, charset='utf8'):
        # self.db = pymysql.connect(host=host,
        #              port=port,
        #              user=user,
        #              password=password,
        #              database=database,
        #              charset=charset)
        self.db = pymysql.connect(user="worker",
                                  passwd="jv1993814",
                                  database="security",
                                  charset="utf8")
        self.cur = None

    def __create_cur(self):  # 一个database可以生成多个游标
        self.cur = self.db.cursor()

    def __create_history(self, in_out=None, car_person=None, visiters_owners=None, address_id=None, plate_number=None,
                         person_id=None):
        '''
        自动生成
        '''
        if car_person == "car":
            self.__create_car_history(in_out, visiters_owners, address_id, plate_number)
        else:
            self.__create_person_history(in_out, visiters_owners, address_id, person_id)

    def history(self):
        '''
        输出所有历史记录
        '''
        try:
            self.__create_cur()
            sql = "select * from history, address where `in/out` !='delete_check' and address.id=history.address_id;"
            self.cur.execute(sql)
            result = []
            for i in self.cur:
                result.append(i)
                print(result)
            self.cur.close()
            return result
        except Exception as e:
            print(e)
            self.db.rollback()
            self.cur.close()
            return False

    #
    # def close(self):
    #     self.db.close()
    #
    def __whether_delete_car(self, plates_number, in_out, owners_visiters):
        if in_out == "out" and owners_visiters == "visiters":
            self.delete_car(plates_number)

    def __whether_delete_person(self, id, in_out, owners_visiters):
        if in_out == "out" and owners_visiters == "visiters":
            self.delete_person_by_id(id)

    def delete_car(self, plate_number):
        '''
        delete_car（业主车辆删除，来访车辆离开后自动删除信息）
        输入 车牌号
        输出(是否删除成功) True False
        '''
        # delete_check
        result = self.check_car(plate_number, "delete_check")
        if not result:
            print('failed')

            return False
        try:
            self.__create_cur()
            sql = "delete from plates where plate_number=%s;"
            self.cur.execute(sql, plate_number)
            self.db.commit()
            self.cur.close()
            print('plates removed')
            return True

        except Exception as e:
            print(e)
            self.db.rollback()
            self.cur.close()
            print('failed')
            return False

    def delete_person_by_id(self, id):
        '''
        delete_person（业主删除，访客离开后自动删除信息）
        输入 人员_id 或 姓名及住址
        输出(是否删除成功) True False
        '''
        try:
            self.__create_cur()
            sql = "delete from owners where id=%s;"
            self.cur.execute(sql, id)
            self.db.commit()
            self.cur.close()
            print('person deleted from the system')
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            self.cur.close()
            return False

    def delete_person_by_address(self, address):
        '''
        delete_person_by_address(住户搬家，所有关于业主的信息清空)
        输入 住址
        输出(成功) True（已删除，或原本没人） False
        '''
        result = self.__whether_address(address)
        if not result:
            print('no such address')
            return False
        address = "云从苑%s%d-%d楼%d层%d室" % (address[0], address[1], address[2], address[3], address[4])

        try:
            self.__create_cur()
            sql = "delete from owners where address_id=(select id from address where address=%s);"
            self.cur.execute(sql, address)
            for i in self.cur:
                print(self.cur)
            self.db.commit()
            self.cur.close()
            print('people relalted deleted from the system or was deleted already.')
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            self.cur.close()
            return False

    def add_car(self, owners_visiters, plate_number, address, tels):
        '''
        add_car(业主车辆登记/来访车辆登记)
        输入 业主/访客 车牌号 住址(参考_address.py) 联系电话 e.g.db.add_car("owners", "浙A323UU", ("梯云纵",1,6,9,1), '12306')
        输出(是否添加成功) True False
        '''
        result = self.__whether_address(address)
        if not result:
            return False
        address = "云从苑%s%d-%d楼%d层%d室" % (address[0], address[1], address[2], address[3], address[4])
        try:
            self.__create_cur()
            sql = "insert into plates (`owners/visiters`, plate_number, tels, address_id) values(%s,%s,%s,(select id from address where address=%s));"
            self.cur.execute(sql, [owners_visiters, plate_number, tels, address])
            self.db.commit()
            self.cur.close()
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            self.cur.close()
            return False

    def add_person(self, owners_visiters, name, tel, address):
        '''
        add_person(业主人员登记/访客登记)
        输入 业主/访客（人员_id） 姓名(访客仅需姓氏性别) 联系方式 住址db.add_person("visiters", "李小姐", '12306',("梯云纵",1,6,9,1))
        输出(是否添加成功) True False
        '''
        result = self.__whether_address(address)
        if not result:
            print('no such address')
            return False
        address = "云从苑%s%d-%d楼%d层%d室" % (address[0], address[1], address[2], address[3], address[4])
        try:
            self.__create_cur()
            sql = "insert into owners (`owners_visiters`, name, tel, address_id) values(%s,%s,%s,(select id from address where address=%s));"
            self.cur.execute(sql, [owners_visiters, name, tel, address])
            i = ""
            for i in self.cur:
                print(i)
            self.db.commit()
            self.cur.close()
        except Exception as e:
            print(e)
            self.db.rollback()
            self.cur.close()
            return False
        print('person added')
        return True

    def check_car(self, plates_number, in_out):
        '''
        check_car(车辆准入/放行)
        输入 车牌号 进/出 e.g. db.check_car("浙A323UU","in")
        输出 False(未登记访客)/True(业主或已登记访客)
        '''

        try:
            self.__create_cur()
            sql = "select `owners/visiters`, plate_number, address_id from plates where plate_number= '%s';" % (
                plates_number)
            self.cur.execute(sql)
            i = ""
            for i in self.cur:
                print("%s,车牌号:%s,住址id：%s" % i, in_out)
                i = i
            self.cur.close()
            if i == "":
                print('check car False')
                return False
            self.__whether_delete_car(plates_number, in_out, i[0])
            return True
        except Exception as e:
            # 车牌不存在local variable 'i' referenced before assignment
            print(e)
            self.db.rollback()
            self.cur.close()
            print('check car False')
            return False

    def get_id(self, name, tel):
        '''
        get_id(人员准入/放行)
        输入 人员_name  tel
        输出 id
        '''

        try:
            self.__create_cur()
            sql = "select id from owners where name='%s' and tel='%s';" % (name, tel)
            self.cur.execute(sql)
            i = ""
            for i in self.cur:
                i = i
            self.cur.close()
        except Exception as e:
            print(e)
            self.db.rollback()
            self.cur.close()
            return False
        return int(i[0])

    def check_person(self, owners_id, in_out):
        '''
        check_person(人员准入/放行)
        输入 人员_id 进/出e.g.result=db.check_person(None/9166,"in")
        输出 False(未登记访客)/True(业主或已登记访客)
        '''

        try:
            self.__create_cur()
            sql = "select * from owners where id='%s';" % (owners_id)
            self.cur.execute(sql)
            i = ""
            for i in self.cur:
                i = i
            self.cur.close()
            if i == "":
                if in_out=='in':
                    print('Forbidden: person not in the system.')
                return False
            print(("id:%s,%s") % (i[0], i[3]), in_out)
            self.__whether_delete_person(owners_id, in_out, i[1])
            self.__create_person_history(in_out,i[1],i[4],owners_id)
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            self.cur.close()
            return False

    def __whether_address(self, address):
        '''
        "云从苑%s%d-%d楼%d层%d室" 范围：
        ("梯云纵","燕子坞","还施水阁"),
        [1,17],[1,6],[1,13)U(13,22],[1,12]
        '''
        try:
            if address[0] in ("梯云纵") and \
                    address[1] in range(1, 18) and \
                    address[2] in range(1, 7) and \
                    (address[3] in range(1, 13) or address[3] in range(14, 23)) and \
                    address[4] in range(1, 13):
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def __create_car_history(self, in_out, visiters_owners, address_id, plate_number):
        try:
            self.__create_cur()
            sql = " insert into history(`in/out`,`car/person`,`visiters/owners`,address_id,plate_number) values(%s,%s,%s,%s,%s);"
            self.cur.execute(sql, [in_out, "car", visiters_owners, address_id, plate_number])
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
        finally:
            self.cur.close()

    def __create_person_history(self, in_out, visiters_owners, address_id, person_id):
        try:
            self.__create_cur()
            sql = " insert into history(`in/out`,`car/person`,`visiters/owners`,address_id,owners_id) values(%s,%s,%s,%s,%s);"
            self.cur.execute(sql, [in_out, "person", visiters_owners, address_id, person_id])
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
        finally:
            self.cur.close()


db = DatabaseModel()
# result=db.add_car("visiters", "浙JNB945", ("梯云纵",1,6,9,1), '12306')
# result=db.check_car("浙JNB945","in")
# result=db.check_car("浙A32322","in")
# result=db.delete_car("浙JNB945")
# result = db.add_person("visiters", "x黄阿玛", '17163245367', ("梯云纵", 4, 2, 9, 11))
# result = db.add_person("owners", "黄阿玛", '17163245367', ("梯云纵", 4, 2, 9, 11))
# result = db.check_person(4, "out")
# result = db.check_person(11, "out")
# result=db.delete_person_by_id(5)
# result=db.delete_person_by_address(("梯云纵",4,2,9,11))
# result = db.get_id("黄阿玛", '17163245367')
# print(result)
# result = db.history()
# print(result)
# nature = "owners"
# uname = "QTX"
# tel = "13958445678"
# adress = ('梯云纵',1,6,9,1)
# db = DatabaseModel()
# print(tuple(adress))
# result = db.add_person(nature,uname,tel,tuple(adress))
# print(result)
