"""
Скрипт для генерации моделей базы данных.
Создайте вашу модель базы данных через psql или pgadmin,
После чего запустите скрипт и он автоматически создаст все необходимые таблицы.

- sabbrumm
"""


import re

from sqlalchemy.orm import declarative_base

from config import config
from database.base import CREDENTIALS

from sqlalchemy import create_engine
from sqlalchemy import MetaData

SYNC_DATABASE_URL = f'postgresql://{CREDENTIALS}/{config.database.database_name()}'
engine = create_engine(SYNC_DATABASE_URL)



metadata = MetaData()
metadata.reflect(engine)
Base = declarative_base()


def camel_to_snake(text):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()

def generate_models():
    modules = []
    for table in metadata.tables.values():
        need_to_import = []

        classes = ""

        classes += f"class {table.name}(base.Base):\n"

        classes += f"\t__tablename__ = \"{table.name}\"\n\n"

        for column in table.columns:
            coltype = column.type.__class__.__name__
            if not column.type.__class__.__name__ in need_to_import:
                need_to_import.append(column.type.__class__.__name__)
            if column.type.__class__.__name__ == "ARRAY":
                coltype = f"ARRAY({column.type.item_type.__class__.__name__})"
                if not column.type.item_type.__class__.__name__ in need_to_import:
                    need_to_import.append(column.type.item_type.__class__.__name__)
            classes += f"\t{column.name} = Column({coltype}," \
                       f" primary_key={column.primary_key}, unique={column.unique}, default={column.default})\n"

        classes += "\n"

        template = ""
        template += "from sqlalchemy import Column, " + ", ".join([str(i) for i in need_to_import]) +"\n"
        template += "from database import base\n\n"
        template += classes
        with open(f"models/tables/{camel_to_snake(table.name)}.py", "w") as f:
            f.write(template)
        modules.append(camel_to_snake(table.name))

    modules = [f"from .{i} import *" for i in modules]
    with open("models/tables/__init__.py", "w") as f:
        f.write("\n\n".join(modules))

def generate_requests():
    requests_output = "from sqlalchemy import select, update, delete\n"\
        "from sqlalchemy.sql.elements import BinaryExpression\n\n"\
        "from database import async_session_factory\n"\
        "from database.models.tables import *\n\n\n"

    for table in metadata.tables.values():
        requests_output+=f"class {table.name}Table(object):\n"

        #create_by_id method
        requests_output+=f"\t@staticmethod\n"
        requests_output+=f"\tasync def create_by_id(id_: int) -> bool:\n"
        requests_output+=f"\t\ttry:\n"
        requests_output+=f"\t\t\tasync with async_session_factory() as session:\n"
        requests_output+=f"\t\t\t\t{camel_to_snake(table.name)}: {table.name} = {table.name}(id=id_)\n"
        requests_output+=f"\t\t\t\tsession.add({camel_to_snake(table.name)})\n"
        requests_output+=f"\t\t\t\tawait session.commit()\n"
        requests_output+=f"\t\t\t\treturn True\n"
        requests_output+=f"\t\texcept Exception as e:\n"
        requests_output+=f"\t\t\tprint(e)\n"
        requests_output += f"\t\t\treturn False\n\n"

        #get_where method
        requests_output+=f"\t@staticmethod\n"
        requests_output+=f"\tasync def get_where(exp: BinaryExpression) -> {table.name} | None:\n"
        requests_output+=f"\t\ttry:\n"
        requests_output+=f"\t\t\tasync with async_session_factory() as session:\n"
        requests_output+=f"\t\t\t\texpression = select({table.name}).where(exp)\n"
        requests_output+=f"\t\t\t\tquery = await session.execute(expression)\n"
        requests_output+=f"\t\t\t\t{camel_to_snake(table.name)}: {table.name} = query.scalar()\n"
        requests_output+=f"\t\t\t\tawait session.close()\n"
        requests_output+=f"\t\t\t\treturn {camel_to_snake(table.name)}\n"
        requests_output+=f"\t\texcept Exception as e:\n"
        requests_output+=f"\t\t\tprint(e)\n"
        requests_output+=f"\t\t\treturn None\n\n"

        #get_by_id method
        requests_output+=f"\t@staticmethod\n"
        requests_output+=f"\tasync def get_by_id(id_: int) -> {table.name} | None:\n"
        requests_output+=f"\t\ttry:\n"
        requests_output+=f"\t\t\tasync with async_session_factory() as session:\n"
        requests_output+=f"\t\t\t\t{camel_to_snake(table.name)}: {table.name} = await session.get({table.name}, id_)\n"
        requests_output+=f"\t\t\t\tawait session.close()\n"
        requests_output+=f"\t\t\t\treturn {camel_to_snake(table.name)}\n"
        requests_output+=f"\t\texcept Exception as e:\n"
        requests_output+=f"\t\t\tprint(e)\n\n"
        requests_output += f"\t\t\treturn None\n\n"

        #update_by_id method
        requests_output+=f"\t@staticmethod\n"
        requests_output+=f"\tasync def update_by_id(id_: int, **kwargs) -> bool:\n"
        requests_output+=f"\t\ttry:\n"
        requests_output+=f"\t\t\tasync with async_session_factory() as session:\n"
        requests_output+=f"\t\t\t\texpression = update({table.name}).where({table.name}.id == id_).values(kwargs)\n"
        requests_output+=f"\t\t\t\tawait session.execute(expression)\n"
        requests_output+=f"\t\t\t\tawait session.commit()\n"
        requests_output+=f"\t\t\t\tawait session.close()\n"
        requests_output+=f"\t\t\t\treturn True\n"
        requests_output+=f"\t\texcept Exception as e:\n"
        requests_output+=f"\t\t\tprint(e)\n\n"
        requests_output += f"\t\t\treturn False\n\n"

        #del_where method
        requests_output+=f"\t@staticmethod\n"
        requests_output+=f"\tasync def del_where(exp: BinaryExpression) -> bool:\n"
        requests_output+=f"\t\ttry:\n"
        requests_output+=f"\t\t\tasync with async_session_factory() as session:\n"
        requests_output+=f"\t\t\t\texpression = delete({table.name}).where(exp)\n"
        requests_output+=f"\t\t\t\tawait session.execute(expression)\n"
        requests_output+=f"\t\t\t\tawait session.commit()\n"
        requests_output+=f"\t\t\t\tawait session.close()\n"
        requests_output+=f"\t\t\t\treturn True\n"
        requests_output+=f"\t\texcept Exception as e:\n"
        requests_output+=f"\t\t\tprint(e)\n\n"
        requests_output += f"\t\t\treturn False\n\n"

        #del_by_id method
        requests_output+=f"\t@staticmethod\n"
        requests_output+=f"\tasync def del_by_id(id_: int) -> bool:\n"
        requests_output+=f"\t\ttry:\n"
        requests_output+=f"\t\t\tasync with async_session_factory() as session:\n"
        requests_output+=f"\t\t\t\texpression = delete({table.name}).where({table.name}.id == id_)\n"
        requests_output += f"\t\t\t\tawait session.execute(expression)\n"
        requests_output+=f"\t\t\t\tawait session.commit()\n"
        requests_output+=f"\t\t\t\tawait session.close()\n"
        requests_output+=f"\t\t\t\treturn True\n"
        requests_output+=f"\t\texcept Exception as e:\n"
        requests_output+=f"\t\t\tprint(e)\n\n"
        requests_output+=f"\t\t\treturn False\n\n\n"
    with open("models/requests.py", "w") as f:
        f.write(requests_output)

if __name__ == "__main__":
    generate_models()
    generate_requests()