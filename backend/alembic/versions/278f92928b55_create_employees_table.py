"""create employees table

Revision ID: 278f92928b55
Revises: 0001_initial_database_foundation
Create Date: 2026-09-19 19:52:45.582650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "278f92928b55"
down_revision: Union[str, Sequence[str], None] = (
    "0001_initial_database_foundation"
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("employee_code", sa.String(length=50), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("country", sa.String(length=100), nullable=False),
        sa.Column("department", sa.String(length=100), nullable=False),
        sa.Column("job_title", sa.String(length=150), nullable=False),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("employee_code"),
        sa.UniqueConstraint("email"),
    )

    op.create_index(
        "ix_employees_employee_code",
        "employees",
        ["employee_code"],
        unique=True,
    )
    op.create_index(
        "ix_employees_email",
        "employees",
        ["email"],
        unique=True,
    )
    op.create_index(
        "ix_employees_country",
        "employees",
        ["country"],
        unique=False,
    )
    op.create_index(
        "ix_employees_department",
        "employees",
        ["department"],
        unique=False,
    )
    op.create_index(
        "ix_employees_status",
        "employees",
        ["status"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_employees_status", table_name="employees")
    op.drop_index("ix_employees_department", table_name="employees")
    op.drop_index("ix_employees_country", table_name="employees")
    op.drop_index("ix_employees_email", table_name="employees")
    op.drop_index("ix_employees_employee_code", table_name="employees")
    op.drop_table("employees")