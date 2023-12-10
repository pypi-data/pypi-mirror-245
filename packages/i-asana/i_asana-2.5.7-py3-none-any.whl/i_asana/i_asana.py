"""Class module to interface with Asana.
"""
# pylint: disable=logging-too-many-args,no-member
# pylint: disable=too-many-arguments,too-many-branches,too-many-instance-attributes

from datetime import date, datetime
import os
import re
from typing import Optional, Union

from aracnid_logger import Logger
import asana
from asana.rest import ApiException

# initialize logging
logger = Logger(__name__).get_logger()


class AsanaInterface:
    """Asana interface class.

    Environment Variables:
        ASANA_ACCESS_TOKEN: Access token for Asana.

    Attributes:
        client: Asana client.

    Exceptions:
        TBD
    """

    def __init__(self) -> None:
        """Initializes the interface.
        """
        # initialize asana client
        configuration = asana.Configuration()
        configuration.access_token = os.environ.get('ASANA_ACCESS_TOKEN')
        self._client = asana.ApiClient(configuration)

        # initialize asana api instances
        self._users = None
        self._tasks = None
        self._task_templates = None
        self._sections = None
        self._projects = None
        self._webhooks = None

        # define default task fields
        self.opt_fields = [
            'assignee',
            'assignee.name',
            'assignee_section',
            'assignee_section.name',
            'completed',
            'completed_at',
            'completed_by',
            'created_at',
            'custom_fields',
            'due_at',
            'due_on',
            'html_notes',
            'memberships.(project|section).name',
            'modified_at',
            'name',
            'notes',
            'num_subtasks',
            'parent',
            'permalink_url',
            'projects',
            'resource_subtype',
            'resource_type',
            'start_at',
            'start_on',
            'tags.name',
            'workspace'        
        ]

        # TODO: set this value programmatically
        self.workspace_id = '1108879292936985'

    @property
    def client(self) -> asana.api_client.ApiClient:
        """Returns the Asana Client object.

        Returns:
            Asana Client object.
        """
        return self._client

    @property
    def users(self) -> asana.api.users_api.UsersApi:
        """Returns an instance of the Users API.
        """
        if not self._users:
            self._users = asana.UsersApi(self.client)

        return self._users

    @property
    def tasks(self) -> asana.api.tasks_api.TasksApi:
        """Returns an instance of the Tasks API.
        """
        if not self._tasks:
            self._tasks = asana.TasksApi(self.client)

        return self._tasks

    @property
    def task_templates(self) -> asana.api.task_templates_api.TaskTemplatesApi:
        """Returns an instance of the Task Templates API.
        """
        if not self._task_templates:
            self._task_templates = asana.TaskTemplatesApi(self.client)

        return self._task_templates

    @property
    def sections(self) -> asana.api.sections_api.SectionsApi:
        """Returns an instance of the Sections API.
        """
        if not self._sections:
            self._sections = asana.SectionsApi(self.client)

        return self._sections

    @property
    def projects(self):
        """Returns an instance of the Projects API.
        """
        if not self._projects:
            self._projects = asana.ProjectsApi(self.client)

        return self._projects

    @property
    def webhooks(self):
        """Returns an instance of the Webhooks API.
        """
        if not self._webhooks:
            self._webhooks = asana.WebhooksApi(self.client)

        return self._webhooks

    @staticmethod
    def url_param(field: str, value: str, field_prefix: str='') -> str:
        """Returns a URL-safe query parameter.

        Args:
            field (str): Name of an Asana table field.
            value (str): Value of an Asana table field.

        Returns:
            str: URL-safe query parameter.
        """
        # make field name
        field_name = field
        if field_prefix:
            field_name = '_'.join((field_prefix, field))

        # make parameter string
        param = f'{field_name}={value}'

        # replace spaces
        param_safe = param.replace(' ', '+')

        return param_safe

    def create_task(self,
            name: str,
            project_id: str,
            start: Union[date, datetime]=None,
            due: Union[date, datetime]=None,
            section_id: str=None,
            parent_id: str=None,
            notes: str='',
            html_notes: str=''
        ) -> asana.models.task_response.TaskResponse:
        """Create a task in the specified project and section

        Start is only set if due is set.

        Args:
            name: Name of the task to create.
            project_id: Project identifier.
            start: Date or date-time when the task will start
            due: Date or date-time when the task is due.
            section_id: (Optional) Section identifier.
            parent_id: (Optional) Parent identifier.
            notes (str): (Optional) Task notes, unformatted.
            html_notes (str): (Optional) Task notes, formatted in HTML.
        """
        task = task_data = None

        # create the task body
        body = {
            'name': name,
            'projects': [project_id]
        }
        if due:
            if isinstance(due, datetime):
                body['due_at'] = due
            elif isinstance(due, date):
                body['due_on'] = due

            if start:
                if isinstance(start, datetime):
                    body['start_at'] = start
                elif isinstance(start, date):
                    body['start_on'] = start
        if notes:
            body['notes'] = notes
        elif html_notes:
            body['html_notes'] = html_notes
        task_body = asana.TasksBody(body)

        # create the task/subtask
        if parent_id:
            try:
                task_body = asana.TaskGidSubtasksBody(body)
                task_data = self.tasks.create_subtask_for_task(task_body, parent_id)
            except ApiException as err:
                logger.error("Exception when calling TasksApi->create_subtask_for_task: %s\n", err)
        else:
            try:
                task_body = asana.TasksBody(body)
                task_data = self.tasks.create_task(task_body)
            except ApiException as err:
                logger.error("Exception when calling TasksApi->create_task: %s\n", err)
        task = task_data.data if task_data else None

        # add task to the specified section
        if task and section_id:
            task_body = asana.SectionGidAddTaskBody({'task': task.gid})
            self.sections.add_task_for_section(
                section_gid=section_id,
                body=task_body
            )

            # retrieve the updated task
            task = self.read_task(task_id=task.gid)

        return task

    def read_task(self,
            task_id: str,
        ) -> Optional[asana.models.task_response.TaskResponse]:
        """Read a task with the specified task id.

        Args:
            task_id: Task identifier.

        Returns:
            Specified task as a dictionary.
        """
        try:
            task = self.tasks.get_task(task_id, opt_fields=self.opt_fields)
            return task.data
        except ApiException as err:
            if err.status == 404:
                logger.warning('Requested task does not exist: %s', task_id)
            else:
                logger.error('Exception when calling TasksApi->read_task: %s\n', err)
        return None

    def update_task(self,
            task_id: str,
            fields: dict,
        ) -> Optional[asana.models.task_response.TaskResponse]:
        """Update the specified task with the new fields.

        Args:
            task_id: Task identifier.
            fields: Fields to updated.

        Returns:
            Updated task as a dictionary.
        """
        try:
            task_body = asana.TasksTaskGidBody(fields)
            task = self.tasks.update_task(task_body, task_gid=task_id, opt_fields=self.opt_fields)
            return task.data
        except ApiException as err:
            if err.status == 404:
                logger.warning('Requested task does not exist: %s', task_id)
            else:
                logger.error("Exception when calling TasksApi->update_task: %s\n", err)
        return None

    def delete_task(self, task_id: str) -> None:
        """Delete a task with the specified task id.

        Args:
            task_id: Task identifier.

        Returns:
            None.
        """
        try:
            self.tasks.delete_task(task_gid=task_id)
        except ApiException as err:
            if err.status == 404:
                logger.warning('Requested task does not exist: %s', task_id)
            else:
                logger.error("Exception when calling TasksApi->delete_task: %s\n", err)

    def read_subtasks(self, task_id: str) -> Optional[list]:
        """Read subtasks for a task with the specified task id.

        Args:
            task_id: Task identifier.

        Returns:
            List of subtasks.
        """
        # get the compact list of subtasks
        try:
            subtasks = self.tasks.get_subtasks_for_task(task_gid=task_id)
        except ApiException as err:
            if err.status == 404:
                logger.warning('Requested task does not exist: %s', task_id)
            else:
                logger.error("Exception when calling TasksApi->get_subtasks_for_task: %s\n", err)
            return None

        # read each full subtask
        subtask_list = []
        for summary_task in subtasks.data:
            subtask_list.append(self.read_task(summary_task.gid))

        return subtask_list

    def read_subtask_by_name(self,
            task_id: str,
            name: str,
            regex: bool=False,
        ) -> Optional[asana.models.task_response.TaskResponse]:
        """Read subtask by name for a task with the specified task id.

        Args:
            task_id (str): Task identifier.
            name (str): Name of the subtask to read or regex pattern if regex is True.
            regex (bool): Indicates if "name" is a regex pattern.

        Returns:
            (dict) Subtask as a dictionary.
        """
        # get the compact list of subtasks
        try:
            subtasks = self.tasks.get_subtasks_for_task(task_gid=task_id)
        except ApiException as err:
            if err.status == 404:
                logger.warning('Requested task does not exist: %s', task_id)
            else:
                logger.error("Exception when calling TasksApi->get_subtasks_for_task: %s\n", err)
            return None

        # read each full subtask
        subtask = None
        for summary_task in subtasks.data:
            if not regex:
                if summary_task.name == name:
                    subtask = self.read_task(summary_task.gid)
                    break

            else:
                if re.match(name, summary_task.name):
                    subtask = self.read_task(summary_task.gid)
                    break

        return subtask

    def create_webhook(self,
            resource: str,
            url: str
        ) -> asana.models.webhook_response.WebhookResponse:
        """Create a webhook for the specified resource.

        Args:
            resource: Identifier of the Asana resource.
            url: Target URL to deliver events from this webhook.

        Returns:
            (WebhookResponse) Created webhook.
        """
        webhook = webhook_data = None

        # create the task body
        body_fields = {
            'resource': resource,
            'target': url
        }

        # create the task/subtask
        try:
            webhook_body = asana.WebhooksBody(body_fields)
            webhook_data = self.webhooks.create_webhook(body=webhook_body)
        except ApiException as err:
            logger.error("Exception when calling WebhooksApi->create_webhook: %s\n", err)
        webhook = webhook_data.data if webhook_data else None

        return webhook

    def read_webhooks(self,
            resource_id: str,
        ) -> list:
        """Returns a set of webhooks associated with the specified resource.

        Args:
            resource_id: Identifier of the Asana resource that contains webhooks.

        Returns:
            (list) List of webhooks.
        """
        try:
            webhook_data = self.webhooks.get_webhooks(
                self.workspace_id,
                resource=resource_id
            )
            return webhook_data.data
        except ApiException as err:
            logger.error('Exception when calling WebhooksApi->get_webhooks: %s\n', err)
        return None

    def read_webhook(self,
            webhook_id: str,
        ) -> asana.models.webhook_response.WebhookResponse:
        """Returns the specified webhook.

        Args:
            webhook_id: Identifier for the specified webhook.

        Returns:
            (WebhookResponse) Webhook object.
        """
        try:
            webhook_data = self.webhooks.get_webhook(
                webhook_gid=webhook_id
            )
            return webhook_data.data
        except ApiException as err:
            logger.error('Exception when calling WebhooksApi->get_webhook: %s\n', err)
        return None

    def delete_webhook(self,
            webhook_id: str,
        ) -> None:
        """Deletes the specified webhook.

        Args:
            webhook_id: Identifier for the specified webhook.
        """
        try:
            self.webhooks.delete_webhook(
                webhook_gid=webhook_id
            )
        except ApiException as err:
            logger.error('Exception when calling WebhooksApi->delete_webhook: %s\n', err)

    def delete_webhooks(self,
            resource_id: str,
        ) -> None:
        """Deletes the specified webhook.

        Args:
            resource: Identifier of the Asana resource.
        """
        try:
            webhook_list = self.read_webhooks(resource_id=resource_id)
            for webhook in webhook_list:
                self.webhooks.delete_webhook(
                    webhook_gid=webhook.gid
                )
        except ApiException as err:
            logger.error('Exception when calling WebhooksApi->delete_webhooks: %s\n', err)
