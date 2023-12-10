import inspect
import json
import os
import sys
import traceback

from dotenv import load_dotenv
load_dotenv()  # noqa: E402
from sdk.src.validate import validate_enviroment_variables
from user_context_remote.user_context import UserContext

from .Component import Component
from .debug_mode import DebugMode
from .fields import Fields
from .LoggerOutputEnum import LoggerOutputEnum
from .MessageSeverity import MessageSeverity
from .SendToLogzIo import SendTOLogzIo
from .Writer import Writer

logzio_token = os.getenv("LOGZIO_TOKEN")
logzio_url = "https://listener.logz.io:8071"
COMPUTER_LANGUAGE = "Python"
loggers = {}


class Logger:  # TODO: should we inherit from python logging instead of all those ugly prints?
    @staticmethod
    def create_logger(**kwargs):
        validate_enviroment_variables()
        mandatory_fields = ('component_id', 'component_name', 'component_category', 'developer_email')
        if not all(k in kwargs['object'] for k in mandatory_fields):
            raise Exception(
                "please insert component_id, component_name, component_category and developer_email in your object")
        component_id = kwargs['object']['component_id']

        if component_id in loggers:
            return loggers.get(component_id)
        else:
            logger = Logger(**kwargs)
            loggers[component_id] = logger
            return logger

    def __init__(self, **kwargs):
        if logzio_token is None:
            raise Exception(
                "Please set in your .env file LOGZIO_TOKEN=cXNHuVkkffkilnkKzZlWExECRlSKqopE")
        self.component_id = kwargs['object']['component_id']
        self.fields = {}
        self._writer = Writer()
        self.logzio_handler = SendTOLogzIo()
        self.writeToSql = False
        self.user_context = None
        self.additional_fields = {}
        self.init(**kwargs)
        DebugMode.init()

    def init(self, log_message=None, **kwargs):
        if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Console, MessageSeverity.Init.value):
            print(f'LoggerService.init(log_message= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            self._insert_variables(**kwargs)
            kwargs['object']['severity_id'] = MessageSeverity.Init.value
            kwargs['object']['severity_name'] = MessageSeverity.Init.name
            kwargs['object']['log_message'] = log_message
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            if self.writeToSql and DebugMode.is_logger_output(
                    self.component_id, LoggerOutputEnum.MySQLDatabase, MessageSeverity.Init.value):
                self._writer.addMessageAndPayload(log_message, **kwargs)
            if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio, MessageSeverity.Init.value):
                self.logzio_handler.send_to_logzio(kwargs['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.Init.value,
                    'severity_name': MessageSeverity.Init.name,
                    'log_message': log_message
                }
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_to_object(**kwargs)
                if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                                  MessageSeverity.Init.value):
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio, MessageSeverity.Init.value):
                    self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    self._insert_variables(**kwargs)
                    kwargs['object']['severity_id'] = MessageSeverity.Init.value
                    kwargs['object']['severity_name'] = MessageSeverity.Init.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    if self.writeToSql and DebugMode.is_logger_output(
                            self.component_id, LoggerOutputEnum.MySQLDatabase, MessageSeverity.Init.value):
                        self._writer.add(**kwargs)
                    if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio,
                                                  MessageSeverity.Init.value):
                        self.logzio_handler.send_to_logzio(kwargs['object'])

    def start(self, log_message=None, **kwargs):
        if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Console, MessageSeverity.Start.value):
            print(f'LoggerService.start(log_message= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Start.value
            kwargs['object']['severity_name'] = MessageSeverity.Start.name
            kwargs['object']['log_message'] = log_message
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self.insert_to_object(**kwargs)
            if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                              MessageSeverity.Start.value):
                self._writer.addMessageAndPayload(log_message, **kwargs)
            if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio, MessageSeverity.Start.value):
                self.logzio_handler.send_to_logzio(kwargs['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.Start.value,
                    'severity_name': MessageSeverity.Start.name,
                    'log_message': log_message
                }
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_to_object(**kwargs)
                if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                                  MessageSeverity.Start.value):
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio, MessageSeverity.Start.value):
                    self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Start.value
                    kwargs['object']['severity_name'] = MessageSeverity.Start.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_to_object(**kwargs)
                    if self.writeToSql and DebugMode.is_logger_output(self.component_id,
                                                                      LoggerOutputEnum.MySQLDatabase,
                                                                      MessageSeverity.Start.value):
                        self._writer.add(**kwargs)
                    if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio,
                                                  MessageSeverity.Start.value):
                        self.logzio_handler.send_to_logzio(kwargs['object'])

    def end(self, log_message=None, **kwargs):
        if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Console, MessageSeverity.End.value):
            print(f'LoggerService.end(log_message= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.End.value
            kwargs['object']['severity_name'] = MessageSeverity.End.name
            kwargs['object']['log_message'] = log_message
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self.insert_to_object(**kwargs)
            if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                              MessageSeverity.End.value):
                self._writer.addMessageAndPayload(log_message, **kwargs)
            if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio, MessageSeverity.End.value):
                self.logzio_handler.send_to_logzio(kwargs['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.End.value,
                    'severity_name': MessageSeverity.End.name,
                    'log_message': log_message
                }
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_to_object(**kwargs)
                if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                                  MessageSeverity.End.value):
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio, MessageSeverity.End.value):
                    self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.End.value
                    kwargs['object']['severity_name'] = MessageSeverity.End.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_to_object(**kwargs)
                    if self.writeToSql and DebugMode.is_logger_output(self.component_id,
                                                                      LoggerOutputEnum.MySQLDatabase,
                                                                      MessageSeverity.End.value):
                        self._writer.add(**kwargs)
                    if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio,
                                                  MessageSeverity.End.value):
                        self.logzio_handler.send_to_logzio(kwargs['object'])

    def exception(self, log_message=None, **kwargs):
        if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Console, MessageSeverity.Exception.value):
            print(f'LoggerService.exception(log_message= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            stack_trace = traceback.format_exception(
                type(kwargs['object']), kwargs['object'], kwargs['object'].__traceback__)
            object_exp = {
                'severity_id': MessageSeverity.Exception.value,
                'severity_name': MessageSeverity.Exception.name,
                'error_stack': f'{str(stack_trace)}',
                'log_message': log_message
            }
            object_exp = self.insert_to_payload_extra_vars(object=object_exp)
            self.insert_to_object(**object_exp)
            if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                              MessageSeverity.Exception.value):
                self._writer.addMessageAndPayload(log_message, **object_exp)
            if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio, MessageSeverity.Exception.value):
                self.logzio_handler.send_to_logzio(object_exp['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.Exception.value,
                    'severity_name': MessageSeverity.Exception.name,
                    'log_message': log_message
                }
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_to_object(**kwargs)
                if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                                  MessageSeverity.Exception.value):
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio,
                                              MessageSeverity.Exception.value):
                    self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    stack_trace = traceback.format_exception(
                        type(kwargs['object']), kwargs['object'], kwargs['object'].__traceback__)
                    object_exp = {
                        'severity_id': MessageSeverity.Exception.value,
                        'severity_name': MessageSeverity.Exception.name,
                        'error_stack': f'{str(stack_trace)}'
                    }
                    object_exp = self.insert_to_payload_extra_vars(object=object_exp)
                    self.insert_to_object(**object_exp)
                    if self.writeToSql and DebugMode.is_logger_output(self.component_id,
                                                                      LoggerOutputEnum.MySQLDatabase,
                                                                      MessageSeverity.Exception.value):
                        self._writer.add(**object_exp)
                    if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio,
                                                  MessageSeverity.Exception.value):
                        self.logzio_handler.send_to_logzio(object_exp['object'])

    def info(self, log_message=None, **kwargs):
        if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Console, MessageSeverity.Information.value):
            print(f'LoggerService.info(log_message= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Information.value
            kwargs['object']['severity_name'] = MessageSeverity.Information.name
            kwargs['object']['log_message'] = log_message
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self.insert_to_object(**kwargs)
            if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                              MessageSeverity.Information.value):
                self._writer.addMessageAndPayload(log_message, **kwargs)
            if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio,
                                          MessageSeverity.Information.value):
                self.logzio_handler.send_to_logzio(kwargs['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.Information.value,
                    'severity_name': MessageSeverity.Information.name,
                    'log_message': log_message
                }
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_to_object(**kwargs)
                if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                                  MessageSeverity.Information.value):
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio,
                                              MessageSeverity.Information.value):
                    self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Information.value
                    kwargs['object']['severity_name'] = MessageSeverity.Information.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_to_object(**kwargs)
                    if self.writeToSql and DebugMode.is_logger_output(self.component_id,
                                                                      LoggerOutputEnum.MySQLDatabase,
                                                                      MessageSeverity.Information.value):
                        self._writer.add(**kwargs)
                    if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio,
                                                  MessageSeverity.Information.value):
                        self.logzio_handler.send_to_logzio(kwargs['object'])

    def error(self, log_message=None, **kwargs):
        if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Console, MessageSeverity.Error.value):
            print(f'LoggerService.error(log_message= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Error.value
            kwargs['object']['severity_name'] = MessageSeverity.Error.name
            kwargs['object']['log_message'] = log_message
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self.insert_to_object(**kwargs)
            if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                              MessageSeverity.Error.value):
                self._writer.addMessageAndPayload(log_message, **kwargs)
            if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio, MessageSeverity.Error.value):
                self.logzio_handler.send_to_logzio(kwargs['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.Error.value,
                    'severity_name': MessageSeverity.Error.name,
                    'log_message': log_message
                }
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_to_object(**kwargs)
                if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                                  MessageSeverity.Error.value):
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio, MessageSeverity.Error.value):
                    self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Error.value
                    kwargs['object']['severity_name'] = MessageSeverity.Error.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_to_object(**kwargs)
                    if self.writeToSql and DebugMode.is_logger_output(self.component_id,
                                                                      LoggerOutputEnum.MySQLDatabase,
                                                                      MessageSeverity.Error.value):
                        self._writer.add(**kwargs)
                    if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio,
                                                  MessageSeverity.Error.value):
                        self.logzio_handler.send_to_logzio(kwargs['object'])

    def warn(self, log_message=None, **kwargs):
        if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Console, MessageSeverity.Warning.value):
            print(f'LoggerService.warn(args= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Warning.value
            kwargs['object']['severity_name'] = MessageSeverity.Warning.name
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self.insert_to_object(**kwargs)
            if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                              MessageSeverity.Warning.value):
                self._writer.addMessageAndPayload(log_message, **kwargs)
            if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio, MessageSeverity.Warning.value):
                self.logzio_handler.send_to_logzio(kwargs['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.Warning.value,
                    'severity_name': MessageSeverity.Warning.name,
                    'log_message': log_message
                }
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_to_object(**kwargs)
                if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                                  MessageSeverity.Warning.value):
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio,
                                              MessageSeverity.Warning.value):
                    self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Warning.value
                    kwargs['object']['severity_name'] = MessageSeverity.Warning.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_to_object(**kwargs)
                    if self.writeToSql and DebugMode.is_logger_output(self.component_id,
                                                                      LoggerOutputEnum.MySQLDatabase,
                                                                      MessageSeverity.Warning.value):
                        self._writer.add(**kwargs)
                    if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio,
                                                  MessageSeverity.Warning.value):
                        self.logzio_handler.send_to_logzio(kwargs['object'])

    def debug(self, log_message=None, **kwargs):
        if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Console, MessageSeverity.Debug.value):
            print(f'LoggerService.debug(log_message= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Debug.value
            kwargs['object']['severity_name'] = MessageSeverity.Debug.name
            kwargs['object']['log_message'] = log_message
            self.insert_to_object(**kwargs)
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                              MessageSeverity.Debug.value):
                self._writer.addMessageAndPayload(log_message, **kwargs)
            if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio, MessageSeverity.Debug.value):
                self.logzio_handler.send_to_logzio(kwargs['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.Debug.value,
                    'severity_name': MessageSeverity.Debug.name,
                    'log_message': log_message
                }
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_to_object(**kwargs)
                if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                                  MessageSeverity.Debug.value):
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio, MessageSeverity.Debug.value):
                    self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Debug.value
                    kwargs['object']['severity_name'] = MessageSeverity.Debug.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_to_object(**kwargs)
                    if self.writeToSql and DebugMode.is_logger_output(self.component_id,
                                                                      LoggerOutputEnum.MySQLDatabase,
                                                                      MessageSeverity.Debug.value):
                        self._writer.add(**kwargs)
                    if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio,
                                                  MessageSeverity.Debug.value):
                        self.logzio_handler.send_to_logzio(kwargs['object'])

    def critical(self, log_message=None, **kwargs):
        if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Console, MessageSeverity.Critical.value):
            print(f'LoggerService.critical(log_message= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Critical.value
            kwargs['object']['severity_name'] = MessageSeverity.Critical.name
            kwargs['object']['log_message'] = log_message
            self.insert_to_object(**kwargs)
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                              MessageSeverity.Critical.value):
                self._writer.addMessageAndPayload(log_message, **kwargs)
            if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio, MessageSeverity.Critical.value):
                self.logzio_handler.send_to_logzio(kwargs['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.Critical.value,
                    'severity_name': MessageSeverity.Critical.name,
                    'log_message': log_message
                }
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_to_object(**kwargs)
                if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                                  MessageSeverity.Critical.value):
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio,
                                              MessageSeverity.Critical.value):
                    self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Critical.value
                    kwargs['object']['severity_name'] = MessageSeverity.Critical.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_to_object(**kwargs)
                    if self.writeToSql and DebugMode.is_logger_output(self.component_id,
                                                                      LoggerOutputEnum.MySQLDatabase,
                                                                      MessageSeverity.Critical.value):
                        self._writer.add(**kwargs)
                    if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio,
                                                  MessageSeverity.Critical.value):
                        self.logzio_handler.send_to_logzio(kwargs['object'])

    def verbose(self, log_message=None, **kwargs):
        if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Console, MessageSeverity.Verbose.value):
            print(f'LoggerService.verbose(log_message= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Verbose.value
            kwargs['object']['severity_name'] = MessageSeverity.Verbose.name
            kwargs['object']['log_message'] = log_message
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self.insert_to_object(**kwargs)
            if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                              MessageSeverity.Verbose.value):
                self._writer.addMessageAndPayload(log_message, **kwargs)
            if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio, MessageSeverity.Verbose.value):
                self.logzio_handler.send_to_logzio(kwargs['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.Verbose.value,
                    'severity_name': MessageSeverity.Verbose.name,
                    'log_message': log_message
                }
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_to_object(**kwargs)
                if self.writeToSql and DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.MySQLDatabase,
                                                                  MessageSeverity.Verbose.value):
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio,
                                              MessageSeverity.Verbose.value):
                    self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Verbose.value
                    kwargs['object']['severity_name'] = MessageSeverity.Verbose.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_to_object(**kwargs)
                    if self.writeToSql and DebugMode.is_logger_output(self.component_id,
                                                                      LoggerOutputEnum.MySQLDatabase,
                                                                      MessageSeverity.Verbose.value):
                        self._writer.add(**kwargs)
                    if DebugMode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio,
                                                  MessageSeverity.Verbose.value):
                        self.logzio_handler.send_to_logzio(kwargs['object'])

    def _insert_variables(self, **kwargs):
        object_data = kwargs.get("object", {})
        for field in self.fields.keys():
            if field in object_data.keys():
                self.fields[field] = object_data[field]
        for field in object_data.keys():
            if field not in self.fields:
                self.additional_fields[field] = object_data.get(field)

    def insert_to_object(self, **kwargs):
        object_data = kwargs.get("object", {})
        for field in self.fields.keys():
            if field not in object_data:
                field_value = self.fields[field]
                if field_value is not None:
                    object_data[field] = field_value

    def get_logger_table_fields(self):
        if self.writeToSql:
            fields = Fields.getFieldsSingelton()
            for field in fields:
                self.fields[field] = None
        return self.fields

    def clean_variables(self):
        for field in self.fields:
            self.fields[field] = None
        self.additional_fields.clear()

    def insert_to_payload_extra_vars(self, **kwargs):
        self.user_context = UserContext.login_using_user_identification_and_password()
        if self.user_context is not None:
            # TODO Shall we change in the database column to real_user_id?
            kwargs['object']['user_id'] = self.user_context.get_real_user_id()
            kwargs['object']['created_user_id'] = self.user_context.get_real_user_id()
            # TODO Shall we change the database to store real_profile_id and effective_profile?
            kwargs['object']['profile_id'] = self.user_context.get_real_profile_id()
            # TODO: change to display_as like we have in contact ...
            if self.user_context.real_display_name is not None:
                # TODO Shall we change current_runner to real_name?
                kwargs['object']['current_runner'] = self.user_context.get_real_name()
            else:
                kwargs['object']['current_runner'] = os.getenv("PRODUCT_USER_IDENTIFIER")
        message = kwargs['object'].pop('message', None)
        kwargs['object']['function_name'] = self.get_current_function_name()
        kwargs['object']['environment'] = os.getenv("ENVIRONMENT_NAME")
        kwargs['object']['class'] = self.get_calling_class()
        kwargs['object']['line_number'] = self.get_calling_line_number()
        kwargs['object']['computer_language'] = COMPUTER_LANGUAGE
        for field in self.fields.keys():
            if field not in kwargs['object']:
                field_value = self.fields[field]
                if field_value is not None:
                    kwargs['object'][field] = field_value
        for field in self.additional_fields.keys():
            if field not in kwargs['object']:
                field_value = self.additional_fields[field]
                kwargs['object'][field] = field_value
        if (self.writeToSql
                and 'component_id' in kwargs['object']
                and 'component_name' not in kwargs['object']):
            component_info = self.get_component_info(kwargs['object']['component_id'])
            if component_info:
                for field in component_info.keys():
                    if field not in kwargs['object']:
                        field_value = component_info[field]
                        if field_value is not None:
                            kwargs['object'][field] = field_value
        if message is not None:
            kwargs['object']['message'] = message
        object_data = kwargs.get("object", {})
        object_data["record"] = json.dumps({key: str(value) for key, value in object_data.items()})
        if self.writeToSql:
            object_data = {key: value for key, value in object_data.items() if key in self.fields.keys()}
            kwargs["object"] = object_data
        return kwargs

    @staticmethod
    def get_current_function_name():
        stack = inspect.stack()
        caller_frame = stack[3]
        function_name = caller_frame.function
        return function_name

    @staticmethod
    def get_calling_class():
        stack = inspect.stack()
        calling_module = inspect.getmodule(stack[3].frame)
        return calling_module.__name__

    @staticmethod
    def get_calling_line_number():
        stack = inspect.stack()
        calling_frame = stack[3]
        line_number = calling_frame.lineno
        return line_number

    def get_component_info(self, component_id):
        result = Component.getDetailsByComponentId(component_id)
        if result:
            name, component_type, component_category, testing_framework, api_type = result
            component_info = {
                'component_name': name,
                'component_type': component_type,
                'component_category': component_category,
                'testing_framework': testing_framework,
                'api_type': api_type
            }
            for field in component_info.keys():
                self.fields[field] = component_info[field]
            return component_info
        else:
            return None

    def isComponentComplete(self):
        return (getattr(self, 'component_name') is None
                or getattr(self, 'component_type') is None
                or getattr(self, 'component_category') is None
                or getattr(self, 'testing_framework') is None
                or getattr(self, 'api_type') is None
                )

    def setWriteToSql(self, value):
        self.writeToSql = value
        if self.writeToSql:
            self.get_logger_table_fields()

    def sql(self):
        sql_query = f"DESCRIBE logger.logger_table"
        try:
            con = self._writer.get_connection()
            cursor = con.cursor()
            cursor.execute(sql_query)
            columns_info = cursor.fetchall()
            columns = [column[0] for column in columns_info]
            return columns
        except Exception as e:
            print("logger-local-python-package LoggerService.py sql(self) Exception caught SQL=" +
                  sql_query + " Exception=" + str(e), file=sys.stderr)
