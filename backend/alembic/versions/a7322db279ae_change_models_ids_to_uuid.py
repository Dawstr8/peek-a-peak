"""change models ids to uuid

Revision ID: a7322db279ae
Revises: 832c2d78a053
Create Date: 2025-12-11 13:00:55.893303

"""

from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
import sqlmodel

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a7322db279ae"
down_revision: Union[str, Sequence[str], None] = "832c2d78a053"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Enable uuid-ossp extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Strategy: Add temporary UUID columns, populate them, then swap
    # This preserves foreign key relationships

    # Step 1: Add temporary UUID columns to all tables with primary keys
    op.execute(
        "ALTER TABLE mountainrange ADD COLUMN id_new UUID DEFAULT gen_random_uuid()"
    )
    op.execute("UPDATE mountainrange SET id_new = gen_random_uuid()")
    op.execute("ALTER TABLE mountainrange ALTER COLUMN id_new SET NOT NULL")

    op.execute("ALTER TABLE peak ADD COLUMN id_new UUID DEFAULT gen_random_uuid()")
    op.execute("UPDATE peak SET id_new = gen_random_uuid()")
    op.execute("ALTER TABLE peak ALTER COLUMN id_new SET NOT NULL")

    op.execute(
        "ALTER TABLE summitphoto ADD COLUMN id_new UUID DEFAULT gen_random_uuid()"
    )
    op.execute("UPDATE summitphoto SET id_new = gen_random_uuid()")
    op.execute("ALTER TABLE summitphoto ALTER COLUMN id_new SET NOT NULL")

    op.execute('ALTER TABLE "user" ADD COLUMN id_new UUID DEFAULT gen_random_uuid()')
    op.execute('UPDATE "user" SET id_new = gen_random_uuid()')
    op.execute('ALTER TABLE "user" ALTER COLUMN id_new SET NOT NULL')

    op.execute(
        "ALTER TABLE weathercondition ADD COLUMN id_new UUID DEFAULT gen_random_uuid()"
    )
    op.execute("UPDATE weathercondition SET id_new = gen_random_uuid()")
    op.execute("ALTER TABLE weathercondition ALTER COLUMN id_new SET NOT NULL")

    op.execute(
        "ALTER TABLE weatherrecord ADD COLUMN id_new UUID DEFAULT gen_random_uuid()"
    )
    op.execute("UPDATE weatherrecord SET id_new = gen_random_uuid()")
    op.execute("ALTER TABLE weatherrecord ALTER COLUMN id_new SET NOT NULL")

    # Step 2: Add temporary UUID columns for foreign keys and populate them
    op.execute("ALTER TABLE peak ADD COLUMN mountain_range_id_new UUID")
    op.execute(
        "UPDATE peak SET mountain_range_id_new = mountainrange.id_new FROM mountainrange WHERE peak.mountain_range_id = mountainrange.id"
    )
    op.execute("ALTER TABLE peak ALTER COLUMN mountain_range_id_new SET NOT NULL")

    op.execute("ALTER TABLE session ADD COLUMN user_id_new UUID")
    op.execute(
        'UPDATE session SET user_id_new = "user".id_new FROM "user" WHERE session.user_id = "user".id'
    )
    op.execute("ALTER TABLE session ALTER COLUMN user_id_new SET NOT NULL")

    op.execute("ALTER TABLE summitphoto ADD COLUMN owner_id_new UUID")
    op.execute(
        'UPDATE summitphoto SET owner_id_new = "user".id_new FROM "user" WHERE summitphoto.owner_id = "user".id'
    )
    op.execute("ALTER TABLE summitphoto ALTER COLUMN owner_id_new SET NOT NULL")

    op.execute("ALTER TABLE summitphoto ADD COLUMN peak_id_new UUID")
    op.execute(
        "UPDATE summitphoto SET peak_id_new = peak.id_new FROM peak WHERE summitphoto.peak_id = peak.id"
    )

    op.execute("ALTER TABLE weatherrecord ADD COLUMN photo_id_new UUID")
    op.execute(
        "UPDATE weatherrecord SET photo_id_new = summitphoto.id_new FROM summitphoto WHERE weatherrecord.photo_id = summitphoto.id"
    )
    op.execute("ALTER TABLE weatherrecord ALTER COLUMN photo_id_new SET NOT NULL")

    op.execute(
        "ALTER TABLE weatherrecordweatherconditionlink ADD COLUMN record_id_new UUID"
    )
    op.execute(
        "UPDATE weatherrecordweatherconditionlink SET record_id_new = weatherrecord.id_new FROM weatherrecord WHERE weatherrecordweatherconditionlink.record_id = weatherrecord.id"
    )
    op.execute(
        "ALTER TABLE weatherrecordweatherconditionlink ALTER COLUMN record_id_new SET NOT NULL"
    )

    op.execute(
        "ALTER TABLE weatherrecordweatherconditionlink ADD COLUMN condition_id_new UUID"
    )
    op.execute(
        "UPDATE weatherrecordweatherconditionlink SET condition_id_new = weathercondition.id_new FROM weathercondition WHERE weatherrecordweatherconditionlink.condition_id = weathercondition.id"
    )
    op.execute(
        "ALTER TABLE weatherrecordweatherconditionlink ALTER COLUMN condition_id_new SET NOT NULL"
    )

    # Step 3: Drop foreign key constraints
    op.execute("ALTER TABLE peak DROP CONSTRAINT IF EXISTS peak_mountain_range_id_fkey")
    op.execute("ALTER TABLE session DROP CONSTRAINT IF EXISTS session_user_id_fkey")
    op.execute(
        "ALTER TABLE summitphoto DROP CONSTRAINT IF EXISTS summitphoto_owner_id_fkey"
    )
    op.execute(
        "ALTER TABLE summitphoto DROP CONSTRAINT IF EXISTS summitphoto_peak_id_fkey"
    )
    op.execute(
        "ALTER TABLE weatherrecord DROP CONSTRAINT IF EXISTS weatherrecord_photo_id_fkey"
    )
    op.execute(
        "ALTER TABLE weatherrecordweatherconditionlink DROP CONSTRAINT IF EXISTS weatherrecordweatherconditionlink_record_id_fkey"
    )
    op.execute(
        "ALTER TABLE weatherrecordweatherconditionlink DROP CONSTRAINT IF EXISTS weatherrecordweatherconditionlink_condition_id_fkey"
    )

    # Step 4: Drop primary key constraints
    op.execute("ALTER TABLE mountainrange DROP CONSTRAINT IF EXISTS mountainrange_pkey")
    op.execute("ALTER TABLE peak DROP CONSTRAINT IF EXISTS peak_pkey")
    op.execute("ALTER TABLE summitphoto DROP CONSTRAINT IF EXISTS summitphoto_pkey")
    op.execute('ALTER TABLE "user" DROP CONSTRAINT IF EXISTS user_pkey')
    op.execute(
        "ALTER TABLE weathercondition DROP CONSTRAINT IF EXISTS weathercondition_pkey"
    )
    op.execute("ALTER TABLE weatherrecord DROP CONSTRAINT IF EXISTS weatherrecord_pkey")

    # Step 5: Drop old columns
    op.execute("ALTER TABLE mountainrange DROP COLUMN id")
    op.execute("ALTER TABLE peak DROP COLUMN id")
    op.execute("ALTER TABLE peak DROP COLUMN mountain_range_id")
    op.execute("ALTER TABLE session DROP COLUMN user_id")
    op.execute("ALTER TABLE summitphoto DROP COLUMN id")
    op.execute("ALTER TABLE summitphoto DROP COLUMN owner_id")
    op.execute("ALTER TABLE summitphoto DROP COLUMN peak_id")
    op.execute('ALTER TABLE "user" DROP COLUMN id')
    op.execute("ALTER TABLE weathercondition DROP COLUMN id")
    op.execute("ALTER TABLE weatherrecord DROP COLUMN id")
    op.execute("ALTER TABLE weatherrecord DROP COLUMN photo_id")
    op.execute("ALTER TABLE weatherrecordweatherconditionlink DROP COLUMN record_id")
    op.execute("ALTER TABLE weatherrecordweatherconditionlink DROP COLUMN condition_id")

    # Step 6: Rename new columns to original names
    op.execute("ALTER TABLE mountainrange RENAME COLUMN id_new TO id")
    op.execute("ALTER TABLE peak RENAME COLUMN id_new TO id")
    op.execute(
        "ALTER TABLE peak RENAME COLUMN mountain_range_id_new TO mountain_range_id"
    )
    op.execute("ALTER TABLE session RENAME COLUMN user_id_new TO user_id")
    op.execute("ALTER TABLE summitphoto RENAME COLUMN id_new TO id")
    op.execute("ALTER TABLE summitphoto RENAME COLUMN owner_id_new TO owner_id")
    op.execute("ALTER TABLE summitphoto RENAME COLUMN peak_id_new TO peak_id")
    op.execute('ALTER TABLE "user" RENAME COLUMN id_new TO id')
    op.execute("ALTER TABLE weathercondition RENAME COLUMN id_new TO id")
    op.execute("ALTER TABLE weatherrecord RENAME COLUMN id_new TO id")
    op.execute("ALTER TABLE weatherrecord RENAME COLUMN photo_id_new TO photo_id")
    op.execute(
        "ALTER TABLE weatherrecordweatherconditionlink RENAME COLUMN record_id_new TO record_id"
    )
    op.execute(
        "ALTER TABLE weatherrecordweatherconditionlink RENAME COLUMN condition_id_new TO condition_id"
    )

    # Step 7: Re-add primary key constraints
    op.execute("ALTER TABLE mountainrange ADD PRIMARY KEY (id)")
    op.execute("ALTER TABLE peak ADD PRIMARY KEY (id)")
    op.execute("ALTER TABLE summitphoto ADD PRIMARY KEY (id)")
    op.execute('ALTER TABLE "user" ADD PRIMARY KEY (id)')
    op.execute("ALTER TABLE weathercondition ADD PRIMARY KEY (id)")
    op.execute("ALTER TABLE weatherrecord ADD PRIMARY KEY (id)")

    # Step 8: Set default values for UUID generation
    op.execute(
        "ALTER TABLE mountainrange ALTER COLUMN id SET DEFAULT gen_random_uuid()"
    )
    op.execute("ALTER TABLE peak ALTER COLUMN id SET DEFAULT gen_random_uuid()")
    op.execute("ALTER TABLE summitphoto ALTER COLUMN id SET DEFAULT gen_random_uuid()")
    op.execute('ALTER TABLE "user" ALTER COLUMN id SET DEFAULT gen_random_uuid()')
    op.execute(
        "ALTER TABLE weathercondition ALTER COLUMN id SET DEFAULT gen_random_uuid()"
    )
    op.execute(
        "ALTER TABLE weatherrecord ALTER COLUMN id SET DEFAULT gen_random_uuid()"
    )

    # Step 9: Re-add foreign key constraints
    op.execute(
        "ALTER TABLE peak ADD CONSTRAINT peak_mountain_range_id_fkey FOREIGN KEY (mountain_range_id) REFERENCES mountainrange(id)"
    )
    op.execute(
        'ALTER TABLE session ADD CONSTRAINT session_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id)'
    )
    op.execute(
        'ALTER TABLE summitphoto ADD CONSTRAINT summitphoto_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES "user"(id)'
    )
    op.execute(
        "ALTER TABLE summitphoto ADD CONSTRAINT summitphoto_peak_id_fkey FOREIGN KEY (peak_id) REFERENCES peak(id)"
    )
    op.execute(
        "ALTER TABLE weatherrecord ADD CONSTRAINT weatherrecord_photo_id_fkey FOREIGN KEY (photo_id) REFERENCES summitphoto(id)"
    )
    op.execute(
        "ALTER TABLE weatherrecordweatherconditionlink ADD CONSTRAINT weatherrecordweatherconditionlink_record_id_fkey FOREIGN KEY (record_id) REFERENCES weatherrecord(id)"
    )
    op.execute(
        "ALTER TABLE weatherrecordweatherconditionlink ADD CONSTRAINT weatherrecordweatherconditionlink_condition_id_fkey FOREIGN KEY (condition_id) REFERENCES weathercondition(id)"
    )

    # Step 10: Drop old sequences
    op.execute("DROP SEQUENCE IF EXISTS mountainrange_id_seq CASCADE")
    op.execute("DROP SEQUENCE IF EXISTS peak_id_seq CASCADE")
    op.execute("DROP SEQUENCE IF EXISTS summitphoto_id_seq CASCADE")
    op.execute("DROP SEQUENCE IF EXISTS user_id_seq CASCADE")
    op.execute("DROP SEQUENCE IF EXISTS weathercondition_id_seq CASCADE")
    op.execute("DROP SEQUENCE IF EXISTS weatherrecord_id_seq CASCADE")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # Note: This downgrade will generate new integer IDs and BREAK existing relationships
    # This is a destructive operation and should only be used in development

    # Step 1: Drop foreign key constraints
    op.execute("ALTER TABLE peak DROP CONSTRAINT IF EXISTS peak_mountain_range_id_fkey")
    op.execute("ALTER TABLE session DROP CONSTRAINT IF EXISTS session_user_id_fkey")
    op.execute(
        "ALTER TABLE summitphoto DROP CONSTRAINT IF EXISTS summitphoto_owner_id_fkey"
    )
    op.execute(
        "ALTER TABLE summitphoto DROP CONSTRAINT IF EXISTS summitphoto_peak_id_fkey"
    )
    op.execute(
        "ALTER TABLE weatherrecord DROP CONSTRAINT IF EXISTS weatherrecord_photo_id_fkey"
    )
    op.execute(
        "ALTER TABLE weatherrecordweatherconditionlink DROP CONSTRAINT IF EXISTS weatherrecordweatherconditionlink_record_id_fkey"
    )
    op.execute(
        "ALTER TABLE weatherrecordweatherconditionlink DROP CONSTRAINT IF EXISTS weatherrecordweatherconditionlink_condition_id_fkey"
    )

    # Step 2: Create sequences
    op.execute("CREATE SEQUENCE IF NOT EXISTS mountainrange_id_seq")
    op.execute("CREATE SEQUENCE IF NOT EXISTS peak_id_seq")
    op.execute("CREATE SEQUENCE IF NOT EXISTS summitphoto_id_seq")
    op.execute("CREATE SEQUENCE IF NOT EXISTS user_id_seq")
    op.execute("CREATE SEQUENCE IF NOT EXISTS weathercondition_id_seq")
    op.execute("CREATE SEQUENCE IF NOT EXISTS weatherrecord_id_seq")

    # Step 3: Convert primary keys back to INTEGER
    op.execute(
        "ALTER TABLE mountainrange ALTER COLUMN id TYPE INTEGER USING nextval('mountainrange_id_seq')"
    )
    op.execute(
        "ALTER TABLE mountainrange ALTER COLUMN id SET DEFAULT nextval('mountainrange_id_seq'::regclass)"
    )

    op.execute(
        "ALTER TABLE peak ALTER COLUMN id TYPE INTEGER USING nextval('peak_id_seq')"
    )
    op.execute(
        "ALTER TABLE peak ALTER COLUMN id SET DEFAULT nextval('peak_id_seq'::regclass)"
    )

    op.execute(
        "ALTER TABLE summitphoto ALTER COLUMN id TYPE INTEGER USING nextval('summitphoto_id_seq')"
    )
    op.execute(
        "ALTER TABLE summitphoto ALTER COLUMN id SET DEFAULT nextval('summitphoto_id_seq'::regclass)"
    )

    op.execute(
        "ALTER TABLE \"user\" ALTER COLUMN id TYPE INTEGER USING nextval('user_id_seq')"
    )
    op.execute(
        "ALTER TABLE \"user\" ALTER COLUMN id SET DEFAULT nextval('user_id_seq'::regclass)"
    )

    op.execute(
        "ALTER TABLE weathercondition ALTER COLUMN id TYPE INTEGER USING nextval('weathercondition_id_seq')"
    )
    op.execute(
        "ALTER TABLE weathercondition ALTER COLUMN id SET DEFAULT nextval('weathercondition_id_seq'::regclass)"
    )

    op.execute(
        "ALTER TABLE weatherrecord ALTER COLUMN id TYPE INTEGER USING nextval('weatherrecord_id_seq')"
    )
    op.execute(
        "ALTER TABLE weatherrecord ALTER COLUMN id SET DEFAULT nextval('weatherrecord_id_seq'::regclass)"
    )

    # Step 4: Convert foreign keys back to INTEGER (will generate new values, breaking relationships)
    op.execute("ALTER TABLE peak ALTER COLUMN mountain_range_id TYPE INTEGER USING 0")
    op.execute("ALTER TABLE session ALTER COLUMN user_id TYPE INTEGER USING 0")
    op.execute("ALTER TABLE summitphoto ALTER COLUMN owner_id TYPE INTEGER USING 0")
    op.execute("ALTER TABLE summitphoto ALTER COLUMN peak_id TYPE INTEGER USING NULL")
    op.execute("ALTER TABLE weatherrecord ALTER COLUMN photo_id TYPE INTEGER USING 0")
    op.execute(
        "ALTER TABLE weatherrecordweatherconditionlink ALTER COLUMN record_id TYPE INTEGER USING 0"
    )
    op.execute(
        "ALTER TABLE weatherrecordweatherconditionlink ALTER COLUMN condition_id TYPE INTEGER USING 0"
    )

    # Note: Foreign key constraints are NOT re-added because the data integrity is broken
    # You would need to manually fix the data and re-add constraints
    # ### end Alembic commands ###
