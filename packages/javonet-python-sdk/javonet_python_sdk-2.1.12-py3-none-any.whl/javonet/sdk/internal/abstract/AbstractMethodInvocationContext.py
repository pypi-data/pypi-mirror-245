import abc


class AbstractMethodInvocationContext(abc.ABC):

    @abc.abstractmethod
    def invoke_static_method(self, string):
        pass

    @abc.abstractmethod
    def get_static_field(self, static_field_name: str):
        pass
