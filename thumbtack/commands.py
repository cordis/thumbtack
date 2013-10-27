from thumbtack.errors import DatabaseSyntaxError


class BaseCommand(object):
    def execute(self, subject):
        raise NotImplementedError()


class SetCommand(BaseCommand):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def execute(self, subject):
        return subject.set(self.name, self.value)


class GetCommand(BaseCommand):
    def __init__(self, name):
        self.name = name

    def execute(self, subject):
        return subject.get(self.name)


class DeleteCommand(BaseCommand):
    def __init__(self, name):
        self.name = name

    def execute(self, subject):
        return subject.delete(self.name)


class GetCountEqualToCommand(BaseCommand):
    def __init__(self, value):
        self.value = value

    def execute(self, subject):
        return subject.get_count_equal_to(self.value)


class BeginTransactionCommand(BaseCommand):
    def execute(self, subject):
        return subject.begin_transaction()


class CommitTransactionCommand(BaseCommand):
    def execute(self, subject):
        return subject.commit_transaction()


class RollbackTransactionCommand(BaseCommand):
    def execute(self, subject):
        return subject.rollback_transaction()


class ExitCommand(BaseCommand):
    def execute(self, subject):
        raise NotImplementedError('Not executable')


class CommandFactory(object):
    name_to_cls_map = {
        'set': SetCommand,
        'get': GetCommand,
        'unset': DeleteCommand,
        'numequalto': GetCountEqualToCommand,
        'begin': BeginTransactionCommand,
        'commit': CommitTransactionCommand,
        'rollback': RollbackTransactionCommand,
        'end': ExitCommand,
    }

    def __call__(self, command_string):
        assert isinstance(command_string, str)
        command_args = filter(None, command_string.split(' '))
        command_name = command_args.pop(0).lower()
        try:
            return self.name_to_cls_map[command_name](*command_args)
        except KeyError:
            raise DatabaseSyntaxError('Command not supported: {0}'.format(command_name))
        except TypeError:
            raise DatabaseSyntaxError('Unexpected number of parameters: {0}'.format(command_name))
