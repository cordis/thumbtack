class BaseOutputCommand(object):
    def execute(self, output_func):
        raise NotImplementedError()


class EmptyOutputCommand(BaseOutputCommand):
    def execute(self, output_func):
        pass


class StringOutputCommand(BaseOutputCommand):
    def __init__(self, output_string):
        self.output_string = str(output_string)

    def execute(self, output_func):
        output_func(self.output_string)
