# -*- coding:utf-8 -*-
from dataclasses import asdict

import pytest

from test.model import Student, Score, Database, Student2


def generate_students(start, end):
    return [
        Student(name=f'李华{i}', age=i, phone=123456789,
                weight=50.0, height=100.0 + i, address=f'hit{i}',
                student_id=i)
        for i in range(start, end)
    ]


student_num = 100
students = [
    Student(name=f'李华{i + 1}', age=i + 1, phone=123456789,
            weight=50.0, height=100.0 + i + 1, address=f'hit{i + 1}',
            student_id=i + 1)
    for i in range(0, student_num)
]


@pytest.mark.order(1)
def test_dao_create_table(init_db: Database):
    """创建表"""
    db = init_db
    db.dao_student._create_table()
    db.dao_score._create_table()
    db.dao_student_info._create_table()
    db.commit()


@pytest.mark.order(2)
def test_insert(init_db):
    """插入数据"""
    db = init_db
    for student in students:
        record_id = db.dao_student.insert(entity=student)
        db.commit()

        result = db.dao_student.select_student_by_id(record_id)
        result = result[0]
        assert result._asdict() == asdict(students[result.student_id - 1])


def test_select_all(init_db):
    """查询全部"""
    db = init_db
    results = db.dao_student.select_all()

    for result in results:
        assert result._asdict() == asdict(students[result.student_id - 1])


def test_select_all_with_substitute(init_db):
    """使用表名替代符"""
    db = init_db
    results = db.dao_student.select_all_with_substitute()

    for result in results:
        assert result._asdict() == asdict(students[result.student_id - 1])


def test_select_student_by_id(init_db):
    """具体查询"""
    db = init_db
    select_id = 50
    result = db.dao_student.select_student_by_id(student_id=select_id)
    assert result[0]._asdict() == asdict(students[select_id - 1])


def test_update_name(init_db):
    """更新"""
    db = init_db
    select_id = 50
    new_name = '好家伙'
    db.dao_student.update_name_by_id(name=new_name, student_id=select_id)
    db.commit()
    result = db.dao_student.select_student_by_id(select_id)
    assert result[0].name == new_name


def test_update_name_with_substitute(init_db):
    """使用表名替代符更新"""
    db = init_db
    select_id = 50
    new_name = '好家伙'
    db.dao_student.update_name_by_id_with_substitute(name=new_name, student_id=select_id)
    db.commit()
    result = db.dao_student.select_student_by_id(select_id)
    assert result[0].name == new_name


def test_multiple_table_substitute(init_db: Database):
    """复杂sql中同时使用多个表名替代符"""
    db = init_db
    result = db.dao_student.select_last_student_with_substitute()
    assert result
    assert result[0].student_id == student_num


def test_foreign_key_cascade(init_db):
    """外键"""
    db = init_db
    db.execute("PRAGMA foreign_keys = ON;")
    select_id = 50
    score = Score(150.0, student_id=select_id)
    db.dao_score.insert(score)
    db.dao_student.delete_student_by_id(student_id=select_id)
    db.commit()

    result = db.dao_score.get_score(select_id)
    assert len(result) == 0


def test_ignore(init_db: Database):
    """数据类的忽略属性在建表时"""
    db = init_db
    db.dao_student2._create_table()
    db.commit()
    db.dao_student2.cursor.execute("PRAGMA table_info(student2);")
    # 获取所有列信息
    columns = db.dao_student2.cursor.fetchall()

    # 提取并打印所有字段名
    columns = set(column[1] for column in columns)
    entity_fields = set(attr_name for attr_name, attr_type in Student2.__annotations__.items())
    ignore_fields = {'score', 'address'}
    entity_fields_without_ignore = set(filter(lambda item: item not in ignore_fields, entity_fields))

    assert entity_fields != columns
    assert entity_fields_without_ignore == columns


def test_insert_ignore(init_db: Database):
    """数据类的忽略属性在插入记录时"""
    db = init_db
    student2 = Student2(name='张三', score=100, address='hit')
    db.dao_student2.insert(student2)
    db.commit()


def test_insert_many(init_db: Database):
    """批量插入"""
    db = init_db
    start = 101
    end = 200
    students2 = generate_students(start=start, end=end)
    db.dao_student.insert(entity=students2)
    db.commit()

    for i in range(start, end):
        result = db.dao_student.select_student_by_id(i)
        result = result[0]
        assert result._asdict() == asdict(students2[i - start])


# ====================================================================================================================

def test_fetchone(init_db: Database):
    """查询单记录"""
    db = init_db
    select_id = 90
    result1 = db.dao_student.select_student_by_id(select_id)
    result2 = db.dao_student.select_student_by_id_limit1(select_id)
    assert isinstance(result1, list)
    assert result1[0] == result2


def test_fetchone_no_record(init_db: Database):
    """查询不存在的单记录"""
    db = init_db
    select_id = 90
    db.dao_student.delete_student_by_id(student_id=select_id)
    result1 = db.dao_student.select_student_by_id(select_id)
    result2 = db.dao_student.select_student_by_id_limit1(select_id)
    assert not result1
    assert result2 is None


# ====================================================================================================================

def test_execute_sql(init_db: Database):
    """执行sql方法"""
    db = init_db
    select_id = 10
    result = db.dao_student.select_one_student(student_id=select_id)
    assert isinstance(result, list)
    assert list
    assert result[0]._asdict() == asdict(students[select_id - 1])


def test_execute_sql_with_substitute(init_db: Database):
    """执行sql方法，使用替代符"""
    db = init_db
    select_id = 10
    result = db.dao_student.select_one_student_with_substitute(student_id=select_id)
    assert result._asdict() == asdict(students[select_id - 1])


def test_execute_sql_with_limit(init_db: Database):
    """执行sql方法，使用limit"""
    db = init_db
    select_id = 10
    result = db.dao_student.select_one_student_with_limit(student_id=select_id)
    assert result._asdict() == asdict(students[select_id - 1])


def test_execute_sql_with_substitute_and_limit(init_db: Database):
    """执行sql方法，使用替代符和limit"""
    db = init_db
    select_id = 10
    result = db.dao_student.select_one_student_with_substitute_and_limit(student_id=select_id)
    assert result._asdict() == asdict(students[select_id - 1])


# ====================================================================================================================

def test_execute_sql_without_dao_func(init_db: Database):
    """执行sql方法"""
    db = init_db
    select_id = 10
    result = db.dao_student3.select_one_student(student_id=select_id)
    assert isinstance(result, list)
    assert list
    assert result[0]._asdict() == asdict(students[select_id - 1])


def test_execute_sql_with_substitute_without_dao_func(init_db: Database):
    """执行sql方法，使用替代符"""
    db = init_db
    select_id = 10
    result = db.dao_student3.select_one_student_with_substitute(student_id=select_id)
    assert result._asdict() == asdict(students[select_id - 1])


def test_execute_sql_with_limit_without_dao_func(init_db: Database):
    """执行sql方法，使用limit"""
    db = init_db
    select_id = 10
    result = db.dao_student3.select_one_student_with_limit(student_id=select_id)
    assert result._asdict() == asdict(students[select_id - 1])


def test_execute_sql_with_substitute_and_limit_without_dao_func(init_db: Database):
    """执行sql方法，使用替代符和limit"""
    db = init_db
    select_id = 10
    result = db.dao_student3.select_one_student_with_substitute_and_limit(student_id=select_id)
    assert result._asdict() == asdict(students[select_id - 1])


def test_execute_sql_with_conditions(init_db: Database):
    """执行sql方法，使用替代符和limit"""
    db = init_db
    select_id = 10
    result = db.dao_student.select_student_with_conditions(student_id=select_id, age=select_id)
    assert result._asdict() == asdict(students[select_id - 1])


if __name__ == '__main__':
    pytest.main(["-vv",
                 "--capture=no",
                 __file__])
