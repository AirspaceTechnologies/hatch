import pytest
from lib.session import Session


@pytest.fixture(autouse=True)
def run_around_tests():
    # Code that will run before each test
    yield
    # Code that will run after each test
    Session().clear()


def test_singleton_behavior():
    session1 = Session()
    session2 = Session()
    assert session1 is session2, "Session instances are not the same (Singleton pattern broken)"


def test_set_and_get():
    session = Session()
    session.set("key1", "value1")
    assert session.get("key1") == "value1", "Failed to retrieve the correct value for 'key1'"


def test_get_with_default():
    session = Session()
    assert (
        session.get("nonexistent_key", "default_value") == "default_value"
    ), "Failed to return default value for nonexistent key"


def test_multiple_sessions():
    session1 = Session()
    session2 = Session()
    session1.set("key2", "value2")
    assert (
        session2.get("key2") == "value2"
    ), "Failed to retrieve the correct value for 'key2' from a second session instance"


def test_add_and_get_thread_ids():
    session = Session()
    session.add_thread_id("thread1")
    session.add_thread_id("thread2")
    assert session.get_thread_ids() == ["thread1", "thread2"], "Failed to retrieve the correct thread IDs"


def test_add_duplicate_thread_id():
    session = Session()
    session.add_thread_id("thread1")
    session.add_thread_id("thread1")
    assert session.get_thread_ids() == ["thread1"], "Duplicate thread IDs were not handled correctly"
