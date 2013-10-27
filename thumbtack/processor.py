from thumbtack.commands import CommandFactory, ExitCommand
from thumbtack.errors import DatabaseError


class RuntimeRunner(object):
    command_factory = CommandFactory()
    command_reader = lambda _: raw_input('>> ')

    def __init__(self, runtime):
        self.runtime = runtime

    def run(self):
        while True:
            command_string = self.command_reader()
            try:
                command = self.command_factory(command_string)
            except DatabaseError as e:
                self.out(e)
                continue
            if isinstance(command, ExitCommand):
                break
            try:
                output_command = self.runtime.execute_command(command)
            except DatabaseError as e:
                self.out(e)
                continue
            else:
                output_command.execute(self.out)

    def out(self, output_string):
        print output_string
