"""create_tables.py will ensure dynamodb tables are created."""
import time
from primal.metadata.models import Entity, Metadata


def update_or_create(model):
    """Will update or create the dynamodb table."""
    if not model.exists():
        model.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True)

    i = 10
    while i >= 0:
        if model.exists():
            return
        else:
            print("Wait for table to be created")
            time.sleep(1)
        i -= 1


def operation():
    """Will run the create_tables operation."""
    update_or_create(Metadata)
    update_or_create(Entity)


if __name__ == "__main__":
    operation()
