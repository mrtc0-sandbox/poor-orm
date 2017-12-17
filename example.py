from poororm import Model, Database, Field

config = {
    'user': 'root',
    'password': 'password',
    'database': 'exampledb',
    'charset': 'utf8'
}

Database.connect(**config)


class UserModel(Model):
    db_table_name = "user"
    id = Field()
    username = Field()
    email = Field()


print(UserModel.all())
# ((1, 'admin', 'admin@example.com'), (2, 'user', 'user@example.com'), (3, 'john', 'john@example.com'))

model = UserModel()
model.username = "mrtc0"
model.email = "mrtc0.py@gmail.com"
model.save()
print(UserModel.all())
# ((1, 'admin', 'admin@example.com'), (2, 'user', 'user@example.com'), (3, 'john', 'john@example.com'), (4, 'mrtc0', 'mrtc0.py@gmail.com'))

print(UserModel.get(id=1, username='admin'))
# (1, 'admin', 'admin@example.com')
