### Migrations can be generated automatically but updates to a type should be handled manually.


1. **Creating a type (ENUM) and dropping manually**:


```python
def upgrade():
    op.execute(
        "CREATE TYPE product_condition_enum AS ENUM('new', 'used', 'open_box', 'damaged');"
    )
    op.add_column(
        "product",
        sa.Column(
            "condition",
            postgresql.ENUM(
                "new",
                "used",
                "open_box",
                "damaged",
                name="product_condition_enum",
                create_type=False,
            ),
            server_default="new",
            nullable=False,
        ),
    )


def downgrade():
    op.drop_column("product", "condition")
    op.execute("DROP TYPE product_condition_enum;")

```

2. **Adding a new value to type (ENUM)**:
```python
def upgrade():
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE product_condition_enum ADD VALUE 'refurbished';")


def downgrade():
    op.execute("UPDATE product SET condition = 'new' WHERE condition = 'refurbished';")
    op.execute(
        "ALTER TYPE product_condition_enum RENAME TO product_condition_enum_temp;"
    )
    op.execute(
        "CREATE TYPE product_condition_enum AS ENUM('new', 'used', 'open_box', 'damaged');"
    )
    op.execute(
        "ALTER TABLE product ALTER COLUMN condition DROP DEFAULT "
    )
    op.execute(
        "ALTER TABLE product ALTER COLUMN condition TYPE product_condition_enum USING condition::text::product_condition_enum "
    )
    op.execute(
        "ALTER TABLE product ALTER COLUMN condition SET DEFAULT 'new'::product_condition_enum"
    )
    op.execute("DROP TYPE product_condition_enum_temp;")
```
