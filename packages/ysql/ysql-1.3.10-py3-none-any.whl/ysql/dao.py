# -*- coding: utf-8 -*-
from ysql.entity import Constraint, _parse_constraints, _Constant
from ysql.tool import log

# ====================================================================================================================
# 模块常量
TABLE_SUBSTITUTE = '__'  # 约定的表名代替符，在sql语句中凡是涉及本表表名的，均可采取此代替符，内部可自动替换。
FETCH_FLAG = 'limit 1'  # 在sql语句中包含此字符，则直接返回Record，不再返回列表。


# ====================================================================================================================
# 装饰器方法
def Dao(entity):
    """对数据访问类使用的装饰器，用于绑定数据类和数据访问类

    Args:
        entity: 该数据访问类对应的数据类

    Example:

        @Entity
        @dataclass
        class Student:  # 定义一个数据类
            name: str
            score: float

        @Dao(Student)  # 通过Dao装饰器绑定对应的数据类
        class DaoStudent:  # 定义一个数据访问类
            ...

    """

    def decorator(cls):
        # 新增cursor属性，可外部直接使用
        setattr(cls, "cursor", None)
        # 新增entity属性
        setattr(cls, "entity", entity)
        # 新增执行sql方法
        setattr(cls, execute_sql.__name__, execute_sql)
        # 新增更新游标方法
        setattr(cls, update_cursor.__name__, update_cursor)
        # 新增创建表方法
        setattr(cls, _create_table.__name__, _create_table)
        # 新增生成表方法
        setattr(cls, _generate_sql_create_table.__name__, _generate_sql_create_table)

        return cls

    return decorator


def Sql(sql: str):
    """执行sql语句的装饰器，传入sql语句的同时会自动实现被装饰函数。

    Args:
        sql: 固定字符串sql语句。

    Example:

        # 对于固定的sql语句可以直接传入Sql装饰器。
        # 此段代码无法直接运行，需要首先连接数据库并插入记录才可运行。

        @Entity
        @dataclass
        class Student:
            name: str
            score: float
            student_id: int = Constraint.auto_primary_key

        @Dao(Student)
        class DaoStudent:

            @Sql("select * from student where student_id=?;")
            def get_student(self, student_id):
                pass  # 此处并非以pass示意省略，而是Sql装饰器会自动实现该函数，因此实际使用时均只需要pass即可。

        dao = DaoStudent()
        result = dao.get_student(student_id=1)

        # 将以列表形式返回查询结果，其中每条记录的数据格式都是具名元组（与数据类类似）
        # result1: [namedtuple('Record', 'name score student_id'), ...]  查询全部字段时，具名元组与定义的数据类完全一致。
        # 查询部分字段时，仅以查询的字段生成相应的具名元组。

    !Note:
        1.对于固定的静态sql语句，通过Sql装饰器传递sql语句，被装饰器函数传递数据。
        2.对于复杂的动态sql语句，不应使用Sql装饰器，应使用dao.execute_sql方法。

    """

    def decorator(func):  # noqa

        def wrapper(self, *args, **kwargs):
            if not isinstance(sql, str):
                raise ValueError(
                    f"传入的sql参数应该是 'str' 类型，但得到的是 '{type(sql).__name__}'类型")

            final_sql = __check_table_substitute(sql=sql, entity=self.entity)
            log.debug(f"生成的执行sql:{final_sql}")

            self.cursor.execute(final_sql, (*args, *kwargs.values()))
            return __fetch_result(sql=final_sql, cursor=self.cursor)

        return wrapper

    if callable(sql):
        raise ValueError(
            f"Sql装饰器需要传入一个 'str' 类型的参数")

    return decorator


def Insert(func):  # noqa
    """执行插入功能的装饰器，会自动生成插入sql语句，以及自动实现被装饰函数。

    Returns:
        自动返回刚插入记录的自增主键（如果使用自增主键）。

    Example:

        # 此段代码无法直接运行，需要首先连接数据库才可运行。

        @Entity
        @dataclass
        class Student:
            name: str
            score: float
            student_id: int = Constraint.auto_primary_key

        @Dao(Student)
        class DaoStudent:

            @Insert  # 无需传递任何参数或者sql语句。
            def insert(self, entity):
                pass  # 此处并非以pass示意省略，而是Insert装饰器会自动实现该函数，因此实际使用时均只需要pass即可。

        dao = DaoStudent()
        # 插入单条记录
        student = Student(name='Bob', score=95.5)  # 将整条记录以数据类的形式插入数据库，避免了同时使用多个参数的麻烦。
        dao.insert(entity=student)
        # 批量插入多条记录
        students = [Student(name='Bob', score=i) for i in range(100)]
        dao.insert(entity=students)
    """

    def wrapper(self, entity):
        """entity参数是传入的数据类实例（对象），而self.entity是定义的数据类（类）"""
        # 获取entity类的属性名和类型
        fields = [field_name for field_name, _ in self.entity.__annotations__.items()]

        # 定义需过滤的属性
        ignore_fields = {Constraint.auto_primary_key.constraint[0],
                         Constraint.ignore.constraint[0]}

        # 过滤属性
        fields = [field_name for field_name in fields
                  if not ignore_fields & set(_parse_constraints(attr_value=getattr(self.entity, field_name, None)))]

        sql = f"insert into {self.entity.__name__} " \
              f"({', '.join(field_name for field_name in fields)}) " \
              f"values ({', '.join('?' for _ in fields)});"
        log.debug(f"生成的插入sql:{sql}")

        if isinstance(entity, self.entity):
            values = [getattr(entity, field_name) for field_name in fields]
            self.cursor.execute(sql, values)
            return self.cursor.lastrowid

        elif isinstance(entity, (list, tuple)):
            values = [[getattr(item, field_name) for field_name in fields]
                      for item in entity]
            self.cursor.executemany(sql, values)
            return
        else:
            raise TypeError(
                f"InsertMany的被装饰函数的参数类型应该是：\n"
                f"1.绑定的Entity数据类的实例\n"
                f"2.包含多个数据类的序列，'list' or 'tuple' "
                f"但得到的是 {type(entity).__name__}")

    return wrapper


# ====================================================================================================================
# 提前实现了一些可用方法的功能类，建议继承。
class DaoFunc:
    """
    Example:
        @Entity
        @dataclass
        class Student:
            name: str
            score: float
            student_id: int = Constraint.auto_primary_key

        @Dao(Student)
        class DaoStudent(DaoFunc):
            pass

    """

    @Insert
    def insert(self, entity):
        """插入单条或多条数据记录

        Args:
            entity: 数据类的实例，或包含多个数据类的序列。

        Returns:
            自动返回刚插入记录的自增主键（如果使用自增主键）。

        """
        pass

    def execute_sql(self, sql: str, params=None):
        """执行sql语句"""
        pass


# ====================================================================================================================
# Dao类需新增的方法
def execute_sql(self, sql: str, params=None):
    """执行sql语句"""
    sql = __check_table_substitute(sql=sql, entity=self.entity)
    if params is None:
        self.cursor.execute(sql)
    elif isinstance(params, _Constant.ENABLED_TYPES):
        self.cursor.execute(sql, (params,))
    elif isinstance(params, (list, tuple)):
        self.cursor.execute(sql, __flatten_params(params))

    return __fetch_result(sql=sql, cursor=self.cursor)


def _create_table(self):
    """依据entity创建表"""
    sql = self._generate_sql_create_table()
    self.cursor.execute(sql)


def update_cursor(self, cursor):
    """更新dao中的游标"""
    self.cursor = cursor


def _generate_sql_create_table(self):
    """自动实现的建表语句"""
    table_name = self.entity.__name__.lower()
    # 获取字段名称和类型的字典
    fields = self.entity.__annotations__

    field_definitions = []
    foreign_key_constraints = []

    for field_name, field_type in fields.items():
        # 获取字段的SQL类型
        sql_type = __convert_to_sql_type(field_type)
        # 获取字段的约束条件
        constraints = _parse_constraints(attr_value=getattr(self.entity, field_name, None))
        # 跳过忽略属性
        if Constraint.ignore.constraint[0] in constraints:
            continue

        foreign_key_constraint = [item for item in constraints
                                  if isinstance(item, tuple)]
        constraints = [item for item in constraints
                       if item not in foreign_key_constraint]
        # 有外键
        if len(foreign_key_constraint) == 1:
            foreign_key_constraint = __generate_sql_foreign_key(field_name=field_name,
                                                                constraint=foreign_key_constraint[0])
            foreign_key_constraints.append(foreign_key_constraint)

        elif len(foreign_key_constraint) > 1:
            raise TypeError(
                '一个属性只能指定一个外键')

        # 合并其他约束条件
        constraint = " ".join(constraints)

        # 拼接字段定义
        field_definition = f"{field_name} {sql_type} {constraint}"
        field_definitions.append(field_definition)
    # 将外键约束列表添加到字段定义列表的末尾
    field_definitions.extend(foreign_key_constraints)
    # 默认为严格的数据类型约束
    sql_create_table = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(field_definitions)});"
    log.debug(f"生成的建表SQL语句：{sql_create_table}")
    return sql_create_table


# ====================================================================================================================
# 模块内的静态方法
def __convert_to_sql_type(python_type):
    """转换python注释类型为sql类型"""
    if python_type in {int, bool}:
        return "INTEGER"
    elif python_type == str:
        return "TEXT"
    elif python_type == float:
        return "REAL"
    elif python_type == bytes:
        return "BLOB"

    raise ValueError(
        f"ysql不支持该python数据类型: {python_type}")  # noqa


def __generate_sql_foreign_key(constraint: tuple, field_name: str):
    """生成外键约束的sql语句"""
    log.debug(f'获得的外键约束：{constraint}')
    foreign_key_entity, foreign_key_name, foreign_key_delete_link, foreign_key_update_link = constraint

    if foreign_key_delete_link is None and foreign_key_update_link is None:
        return f"FOREIGN KEY ({field_name}) " \
               f"REFERENCES {foreign_key_entity}({foreign_key_name})"

    # 存在表关联的情况
    elif foreign_key_delete_link is not None and foreign_key_update_link is None:
        return f"FOREIGN KEY ({field_name}) " \
               f"REFERENCES {foreign_key_entity}({foreign_key_name}) ON DELETE {foreign_key_delete_link}"
    elif foreign_key_delete_link is None and foreign_key_update_link is not None:
        return f"FOREIGN KEY ({field_name}) " \
               f"REFERENCES {foreign_key_entity}({foreign_key_name}) ON UPDATE {foreign_key_update_link}"
    elif foreign_key_delete_link is not None and foreign_key_update_link is not None:
        return f"FOREIGN KEY ({field_name}) " \
               f"REFERENCES {foreign_key_entity}({foreign_key_name}) " \
               f"ON DELETE {foreign_key_delete_link} ON UPDATE {foreign_key_update_link} "


def __check_table_substitute(sql: str, entity):
    """检查并替换表名代替符"""
    return sql.replace(TABLE_SUBSTITUTE, entity.__name__.upper())


def __fetch_result(sql, cursor):
    # 确定返回形式
    if FETCH_FLAG in sql.lower():
        return cursor.fetchone()
    return cursor.fetchall()


def __flatten_params(params):
    """一维展开不定参数，并返回元组形式"""

    def flatten_args(arg):
        if isinstance(arg, (list, tuple)):
            # 如果是列表或元组，递归展开每个元素
            return [item for sublist in map(flatten_args, arg) for item in sublist]
        elif isinstance(arg, dict):
            # 如果是字典，取出所有值并递归展开
            return flatten_args(list(arg.values()))
        elif isinstance(arg, _Constant.ENABLED_TYPES):
            # 否则返回单个值
            return [arg]
        else:
            raise ValueError(
                f"params参数的类型应该是 'list' or 'tuple' or 'dict' ,但得到的是 '{type(arg).__name__}'"
            )

    return tuple(flatten_args(params))
