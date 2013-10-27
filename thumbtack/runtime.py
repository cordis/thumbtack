from thumbtack.storage_states import PersistentStorageState
from thumbtack.output import EmptyOutputCommand, StringOutputCommand


class Runtime(object):
    def __init__(self, storage):
        self.state = PersistentStorageState(storage)

    def execute_command(self, command):
        self.state.append_command(command)
        return command.execute(self)

    def set(self, name, value):
        self.state.set(name, value)
        return EmptyOutputCommand()

    def get(self, name):
        ret = self.state.get(name)
        return StringOutputCommand(ret)

    def delete(self, name):
        self.state.delete(name)
        return EmptyOutputCommand()

    def get_count_equal_to(self, value):
        ret = self.state.get_count_equal_to(value)
        return StringOutputCommand(ret)

    def begin_transaction(self):
        self.state = self.state.begin_transaction()
        return EmptyOutputCommand()

    def commit_transaction(self):
        self.state = self.state.commit_transaction()
        return EmptyOutputCommand()

    def rollback_transaction(self):
        self.state = self.state.rollback_transaction()
        return EmptyOutputCommand()
