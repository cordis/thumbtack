from collections import deque, defaultdict

from thumbtack.errors import DatabaseStateError
from thumbtack.storage import Storage


class PersistentStorageState(object):
    def __init__(self, storage):
        self.storage = storage

    def set(self, name, value):
        self.storage.set(name, value)

    def get(self, name):
        return self.storage.get(name)

    def delete(self, name):
        self.storage.delete(name)

    def get_count_equal_to(self, value):
        return self.storage.get_count_equal_to(value)

    def append_command(self, command):
        pass

    def begin_transaction(self):
        return TransactionStorageState(self)

    def commit_transaction(self):
        raise DatabaseStateError('No transaction')

    def rollback_transaction(self):
        raise DatabaseStateError('No transaction')


class TransactionStorageState(object):
    parent = None
    commands = None

    def __init__(self, parent):
        self.parent = parent
        self.storage = Storage()
        self.deleted = defaultdict()
        self.commands = deque()

    def append_command(self, command):
        self.commands.append(command)

    def set(self, name, value):
        self.storage.set(name, value)
        self.deleted.pop(name, None)

    def get(self, name):
        if name in self.deleted:
            return None
        return self.storage.get(name) or self.parent.get(name)

    def delete(self, name):
        if name not in self.deleted:
            self.deleted[name] = self.get(name)
            self.storage.delete(name)

    def get_count_equal_to(self, value):
        self_count = self.storage.get_count_equal_to(value)
        parent_count = self.parent.get_count_equal_to(value)
        deleted_count = len(filter(lambda v: v == value, self.deleted.values()))
        return self_count + parent_count - deleted_count

    def begin_transaction(self):
        return type(self)(self)

    def commit_transaction(self):
        if isinstance(self.parent, type(self)):
            state = self.parent.commit_transaction()
        else:
            state = self.parent
        while len(self.commands) > 1:
            command = self.commands.popleft()
            command.execute(state.storage)
        return state

    def rollback_transaction(self):
        state = self.parent
        if isinstance(state, type(self)):
            state.commands.pop()
        return state
