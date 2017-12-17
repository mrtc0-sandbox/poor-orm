import MySQLdb


class Field(object):
    pass


class MetaModel(type):
    db_table_name = None
    fields = {}

    def __init__(cls, name, bases, attrs):
        super(MetaModel, cls).__init__(name, bases, attrs)
        fields = {}
        for key, val in cls.__dict__.items():
            if isinstance(val, Field):
                fields[key] = val
        cls.fields = fields
        cls.attrs = attrs


class Model(object, metaclass=MetaModel):
    # Model

    @classmethod
    def all(cls):
        # fetch all records
        sql = 'SELECT * FROM %s;' % cls.db_table_name
        return Database.execute(sql).fetchall()

    @classmethod
    def get(cls, **kwargs):
        e = ["%s = '%s'" % (k, v) for k, v in kwargs.items()]
        sql = 'SELECT * FROM %s WHERE %s' % (cls.db_table_name, ' AND '.join(e))
        return Database.execute(sql).fetchone()

    def save(self):
        sql = 'INSERT IGNORE INTO %s(%s) VALUES (%s);' % (
            self.db_table_name,
            ', '.join(self.__dict__.keys()),
            ', '.join(['%s'] * len(self.__dict__))
        )
        # INSRT IGNORE INTO `table_name`(key1, key2) VALUES (%s %s...)
        return Database.execute(sql, self.__dict__.values())


class Database(object):

    conn = None
    autocommit = True

    @classmethod
    def connect(cls, **config):
        # Connect Database
        cls.conn = MySQLdb.connect(
            user=config.get('user', 'root'),
            passwd=config.get('password', ''),
            db=config.get('database', 'test'),
            charset=config.get('charset', 'utf8')
        )
        cls.conn.autocommit(cls.autocommit)

    @classmethod
    def execute(cls, *args):
        c = cls.conn.cursor()
        c.execute(*args)
        return c

    def __del__(self):
        if self.conn and self.conn.open:
            self.conn.close()
