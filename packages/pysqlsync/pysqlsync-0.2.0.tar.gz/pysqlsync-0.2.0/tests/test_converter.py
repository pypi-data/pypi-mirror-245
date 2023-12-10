import copy
import unittest

from pysqlsync.formation.mutation import Mutator, MutatorOptions
from pysqlsync.formation.object_types import Column, StructMember, UniqueConstraint
from pysqlsync.formation.py_to_sql import (
    ENUM_NAME_LENGTH,
    DataclassConverter,
    DataclassConverterOptions,
    EnumMode,
    NamespaceMapping,
    StructMode,
    dataclass_to_struct,
    dataclass_to_table,
    module_to_catalog,
)
from pysqlsync.formation.sql_to_py import SqlConverterOptions, table_to_dataclass
from pysqlsync.model.data_types import (
    SqlDoubleType,
    SqlFixedCharacterType,
    SqlIntegerType,
    SqlUserDefinedType,
    SqlUuidType,
    SqlVariableCharacterType,
)
from pysqlsync.model.id_types import LocalId, QualifiedId
from pysqlsync.python_types import dataclass_to_code
from tests import empty, tables


class TestConverter(unittest.TestCase):
    def test_primary_key(self) -> None:
        table_def = dataclass_to_table(tables.Address)
        self.assertListEqual(
            list(table_def.columns.values()),
            [
                Column(LocalId("id"), SqlIntegerType(8), False),
                Column(LocalId("city"), SqlVariableCharacterType(), False),
                Column(LocalId("state"), SqlVariableCharacterType(), True),
            ],
        )

    def test_identity(self) -> None:
        table_def = dataclass_to_table(tables.UniqueTable)
        self.assertListEqual(
            list(table_def.columns.values()),
            [
                Column(LocalId("id"), SqlIntegerType(8), False, identity=True),
                Column(LocalId("unique"), SqlVariableCharacterType(64), False),
            ],
        )
        self.assertListEqual(
            list(table_def.constraints.values()),
            [UniqueConstraint(LocalId("uq_UniqueTable_unique"), LocalId("unique"))],
        )

    def test_foreign_key(self) -> None:
        options = DataclassConverterOptions(namespaces=NamespaceMapping({tables: None}))
        table_def = dataclass_to_table(tables.Person, options=options)
        self.assertEqual(table_def.name, QualifiedId(None, "Person"))
        self.assertEqual(table_def.description, "A person.")
        self.assertListEqual(
            list(table_def.columns.values()),
            [
                Column(LocalId("id"), SqlIntegerType(8), False),
                Column(
                    LocalId("name"),
                    SqlVariableCharacterType(),
                    False,
                    description="The person's full name.",
                ),
                Column(
                    LocalId("address"),
                    SqlIntegerType(8),
                    False,
                    description="The address of the person's permanent residence.",
                ),
            ],
        )

    def test_recursive_table(self) -> None:
        table_def = dataclass_to_table(tables.Employee)
        self.assertListEqual(
            list(table_def.columns.values()),
            [
                Column(LocalId("id"), SqlUuidType(), False),
                Column(LocalId("name"), SqlVariableCharacterType(), False),
                Column(LocalId("reports_to"), SqlUuidType(), False),
            ],
        )

    def test_enum_type(self) -> None:
        options = DataclassConverterOptions(
            enum_mode=EnumMode.TYPE, namespaces=NamespaceMapping({tables: None})
        )
        table_def = dataclass_to_table(tables.EnumTable, options=options)
        self.assertListEqual(
            list(table_def.columns.values()),
            [
                Column(LocalId("id"), SqlIntegerType(8), False),
                Column(
                    LocalId("state"),
                    SqlUserDefinedType(QualifiedId(None, "WorkflowState")),
                    False,
                ),
                Column(
                    LocalId("optional_state"),
                    SqlUserDefinedType(QualifiedId(None, "WorkflowState")),
                    True,
                ),
            ],
        )

    def test_enum_relation(self) -> None:
        options = DataclassConverterOptions(
            enum_mode=EnumMode.RELATION, namespaces=NamespaceMapping({tables: None})
        )
        converter = DataclassConverter(options=options)
        catalog = converter.dataclasses_to_catalog([tables.EnumTable])
        table_def = catalog.get_table(QualifiedId(None, tables.EnumTable.__name__))
        self.assertListEqual(
            list(table_def.columns.values()),
            [
                Column(LocalId("id"), SqlIntegerType(8), False),
                Column(LocalId("state"), SqlIntegerType(4), False),
                Column(LocalId("optional_state"), SqlIntegerType(4), True),
            ],
        )
        enum_def = catalog.get_table(QualifiedId(None, tables.WorkflowState.__name__))
        self.assertListEqual(
            list(enum_def.columns.values()),
            [
                Column(LocalId("id"), SqlIntegerType(4), False, identity=True),
                Column(
                    LocalId("value"), SqlVariableCharacterType(ENUM_NAME_LENGTH), False
                ),
            ],
        )

    def test_literal_type(self) -> None:
        options = DataclassConverterOptions(namespaces=NamespaceMapping({tables: None}))
        table_def = dataclass_to_table(tables.LiteralTable, options=options)
        self.assertListEqual(
            list(table_def.columns.values()),
            [
                Column(LocalId("id"), SqlIntegerType(8), False),
                Column(
                    LocalId("single"),
                    SqlFixedCharacterType(limit=5),
                    False,
                ),
                Column(
                    LocalId("multiple"),
                    SqlFixedCharacterType(limit=4),
                    False,
                ),
                Column(
                    LocalId("union"),
                    SqlVariableCharacterType(limit=255),
                    False,
                ),
                Column(
                    LocalId("unbounded"),
                    SqlVariableCharacterType(),
                    False,
                ),
            ],
        )

    def test_struct_definition(self) -> None:
        struct_def = dataclass_to_struct(tables.Coordinates)
        self.assertEqual(
            struct_def.description, "Coordinates in the geographic coordinate system."
        )
        self.assertListEqual(
            list(struct_def.members.values()),
            [
                StructMember(LocalId("lat"), SqlDoubleType(), "Latitude in degrees."),
                StructMember(LocalId("long"), SqlDoubleType(), "Longitude in degrees."),
            ],
        )

    def test_struct_reference(self) -> None:
        table_def = dataclass_to_table(
            tables.Location,
            options=DataclassConverterOptions(struct_mode=StructMode.TYPE),
        )
        self.assertListEqual(
            list(table_def.columns.values()),
            [
                Column(LocalId("id"), SqlIntegerType(8), False),
                Column(
                    LocalId("coords"),
                    SqlUserDefinedType(
                        QualifiedId(tables.__name__, tables.Coordinates.__name__)
                    ),
                    False,
                ),
            ],
        )

    def test_module(self) -> None:
        catalog = module_to_catalog(
            tables,
            options=DataclassConverterOptions(
                enum_mode=EnumMode.CHECK,
                struct_mode=StructMode.JSON,
                namespaces=NamespaceMapping({tables: "public"}),
            ),
        )
        for table in catalog.namespaces["public"].tables.values():
            cls = table_to_dataclass(table, SqlConverterOptions({"public": empty}))
            str(dataclass_to_code(cls))

    def test_mutate(self) -> None:
        source = module_to_catalog(
            tables,
            options=DataclassConverterOptions(
                enum_mode=EnumMode.TYPE,
                struct_mode=StructMode.TYPE,
                namespaces=NamespaceMapping({tables: "public"}),
            ),
        )
        target = copy.deepcopy(source)
        target_ns = target.namespaces["public"]
        target_ns.enums["WorkflowState"].values.append("unknown")
        target_ns.structs.remove("Coordinates")
        target_ns.tables.remove("Employee")
        target_ns.tables["UserTable"].columns.remove("homepage_url")
        target_ns.tables["UserTable"].columns["short_name"].nullable = True
        target_ns.tables["UserTable"].columns.add(
            Column(LocalId("social_url"), SqlVariableCharacterType(), False)
        )
        self.assertEqual(
            Mutator().mutate_catalog_stmt(source, target),
            'ALTER TYPE "public"."WorkflowState"\n'
            "ADD VALUE 'unknown';\n"
            'ALTER TABLE "public"."UserTable"\n'
            'ADD COLUMN "social_url" text NOT NULL,\n'
            'ALTER COLUMN "short_name" DROP NOT NULL,\n'
            'DROP COLUMN "homepage_url";\n'
            'DROP TABLE "public"."Employee";\n'
            'DROP TYPE "public"."Coordinates";',
        )
        self.assertEqual(
            Mutator(
                MutatorOptions(
                    allow_drop_enum=False,
                    allow_drop_struct=False,
                    allow_drop_table=False,
                    allow_drop_namespace=False,
                )
            ).mutate_catalog_stmt(source, target),
            'ALTER TYPE "public"."WorkflowState"\n'
            "ADD VALUE 'unknown';\n"
            'ALTER TABLE "public"."UserTable"\n'
            'ADD COLUMN "social_url" text NOT NULL,\n'
            'ALTER COLUMN "short_name" DROP NOT NULL,\n'
            'DROP COLUMN "homepage_url";',
        )


if __name__ == "__main__":
    unittest.main()
