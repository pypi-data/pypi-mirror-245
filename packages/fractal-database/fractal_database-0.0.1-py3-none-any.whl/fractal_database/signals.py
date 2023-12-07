import logging
import os
import threading
from typing import TYPE_CHECKING, Dict, List

from asgiref.sync import async_to_sync
from django.conf import settings
from django.db import transaction
from django.db.models import F

logger = logging.getLogger("django")

_thread_locals = threading.local()

if TYPE_CHECKING:
    from fractal_database.models import Database, ReplicatedModel, ReplicationTarget


def enter_signal_handler():
    """Increments the counter indicating we've entered a new signal handler."""
    if not hasattr(_thread_locals, "signal_nesting_count"):
        _thread_locals.signal_nesting_count = 0
    _thread_locals.signal_nesting_count += 1


def exit_signal_handler():
    """Decrements the counter indicating we've exited a signal handler."""
    _thread_locals.signal_nesting_count -= 1


def in_nested_signal_handler():
    """Returns True if we're in a nested signal handler, False otherwise."""
    return getattr(_thread_locals, "signal_nesting_count", 0) > 1


def commit(target: "ReplicationTarget") -> None:
    """
    Commits a deferred replication for a ReplicationTarget, then removes
    the ReplicationTarget from deferred replications.

    Intended to be called by the transaction.on_commit handler registered
    by defer_replication.
    """
    # this runs its own thread so once this completes, we need to clear the deferred replications
    # for this target
    async_to_sync(target.replicate)()
    clear_deferred_replications(target.name)


def defer_replication(target: "ReplicationTarget") -> None:
    """
    Defers replication of a ReplicationTarget until the current transaction is committed.
    Supports multiple ReplicationTargets per transaction. Replication will only be performed
    once per target.

    Args:
        target (ReplicationTarget): The ReplicationTarget to defer replication.
    """
    if not transaction.get_connection().in_atomic_block:
        raise Exception("Replication can only be deferred inside an atomic block")

    logger.info(f"Deferring replication of {target}")
    if not hasattr(_thread_locals, "defered_replications"):
        _thread_locals.defered_replications = {}
    # only register an on_commit replicate once per target
    if target.name not in _thread_locals.defered_replications:
        logger.info(f"Registering on_commit for {target.name}")
        transaction.on_commit(lambda: commit(target))
    _thread_locals.defered_replications.setdefault(target.name, []).append(target)


def get_deferred_replications() -> Dict[str, List["ReplicationTarget"]]:
    """
    Returns a dict of ReplicationTargets that have been deferred for replication.
    """
    return getattr(_thread_locals, "defered_replications", {})


def clear_deferred_replications(target: str) -> None:
    """
    Clears the deferred replications for a given target.

    Args:
        target (str): The target to clear deferred replications for.
    """
    logger.info("Clearing deferred replications for target %s" % target)
    del _thread_locals.defered_replications[target]


def increment_version(sender, instance, **kwargs) -> None:
    """
    Increments the object version and updates the last_updated_by field to the
    configured owner in settings.py
    """
    # instance = sender.objects.select_for_update().get(uuid=instance.uuid)
    # TODO set last updated by when updating
    instance.update(object_version=F("object_version") + 1)
    instance.refresh_from_db()


def launch_replication_agent(
    sender: "Database", instance: "Database", created: bool, raw: bool, **kwargs
) -> None:
    if instance.database:
        # check which type of replication agent to launch
        target = instance.database.replicationtarget_set.filter(primary=True)[0]
        target.module.launch()
        logger.info(f"Launching replication agent for {instance.database} using {target.module}")


def object_post_save(
    sender: "ReplicatedModel", instance: "ReplicatedModel", created: bool, raw: bool, **kwargs
) -> None:
    """
    Schedule replication for a ReplicatedModel instance
    """
    if raw:
        logger.info(f"Loading instance from fixture: {instance}")
        return None

    if not transaction.get_connection().in_atomic_block:
        with transaction.atomic():
            return object_post_save(sender, instance, created, raw, **kwargs)

    logger.debug("in atomic block")

    enter_signal_handler()

    increment_version(sender, instance)

    try:
        if in_nested_signal_handler():
            logger.info(f"Back inside post_save for instance: {instance}")
            return None

        logger.info(f"Outermost post save instance: {instance}")

        from fractal_database.models import (
            Database,
            DummyReplicationTarget,
            RootDatabase,
        )

        if isinstance(instance, RootDatabase) or isinstance(instance, Database):
            database = instance
        else:
            database = instance.database
        # create a dummy replication target if none exists so we can replicate when a real target is added
        if not database.replicationtarget_set.exists():  # type: ignore
            DummyReplicationTarget.objects.create(
                name="dummy",
                database=database,
                primary=False,
            )
        # create replication log entry for this instance
        logger.info(f"Calling schedule replication on {instance}")
        instance.schedule_replication(created=created)

    finally:
        exit_signal_handler()


def set_object_database(
    sender: "ReplicatedModel", instance: "ReplicatedModel", raw: bool, **kwargs
) -> None:
    """
    Set the database for a user defined model
    """
    if raw:
        return

    from fractal_database.models import Database, RootDatabase

    if isinstance(instance, RootDatabase):
        try:
            database = RootDatabase.objects.get()
            raise Exception("Only one root database can exist in a root database")
        except RootDatabase.DoesNotExist:
            instance.database = instance  # type: ignore
            return

    try:
        root_database = RootDatabase.objects.get()
        # if this object is a database inside a root database set the database to RootDatabase
        instance.database = root_database
        return
    except RootDatabase.DoesNotExist:
        # in an instance database
        # get the sole Database and set it as the database for this object
        if isinstance(instance, Database):
            try:
                database = Database.objects.get()
                # return if current instance is the sole existing database
                if database == instance:
                    return
                raise Exception("Only one database can exist in an instance database")
            except Database.DoesNotExist:
                return

        # set the database to the sole Database on the user defined model
        database = Database.objects.get()
        instance.database = database


def create_project_database(*args, **kwargs) -> None:
    """
    Runs on post_migrate signal to create the Fractal Database for the Django project
    """
    from fractal_database.models import RootDatabase

    project_name = os.path.basename(settings.BASE_DIR)
    logger.info('Creating Fractal Database for Django project "%s"' % project_name)
    RootDatabase.objects.get_or_create(name=project_name, defaults={"name": project_name})


def create_matrix_replication_target(*args, **kwargs) -> None:
    """
    Runs on post_migrate signal to setup the MatrixReplicationTarget for the Django project
    """
    from fractal_database.models import RootDatabase
    from fractal_database_matrix.models import MatrixReplicationTarget

    # make sure the appropriate matrix env vars are set
    homeserver_url = os.environ["MATRIX_HOMESERVER_URL"]
    access_token = os.environ["MATRIX_ACCESS_TOKEN"]
    project_name = os.path.basename(settings.BASE_DIR)
    database = RootDatabase.objects.get(name=project_name)

    logger.info("Creating MatrixReplicationTarget for database %s" % database)

    target, created = MatrixReplicationTarget.objects.get_or_create(
        name="matrix",
        defaults={
            "name": "matrix",
            "primary": True,
            "database": database,
            "homeserver": homeserver_url,
            "access_token": access_token,
        },
    )

    # replicate the database to the new created MatrixReplicationTarget
    logger.info("Replicating %s to %s" % (database, target))
    # call schedule_replication with created True so the representation will
    # be created on the Matrix homeserver
    database.schedule_replication(created=created)
