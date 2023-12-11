#!/usr/bin/env python3

# Standard libraries
from argparse import Namespace
from json import load as json_load
from os import environ
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Modules libraries
try:
    from questionary import (
        checkbox as questionary_checkbox,
        select as questionary_select,
        text as questionary_text,
        Choice as questionary_Choice,
        Separator as questionary_Separator,
    )
except ModuleNotFoundError: # pragma: no cover
    pass

# Components
from ..package.bundle import Bundle
from ..prints.colors import Colors
from ..prints.themes import Themes
from ..system.platform import Platform
from ..types.dicts import Dicts
from ..types.lists import Lists
from ..types.yaml import YAML
from .pipelines import PipelinesFeature

# MenusFeature class
class MenusFeature:

    # Members
    __jobs: Dict[str, Dict[str, Any]]
    __options: Namespace

    # Constructor
    def __init__(self, jobs: Dict[str, Dict[str, Any]], options: Namespace) -> None:

        # Prepare jobs
        self.__jobs = jobs

        # Prepare options
        self.__options = options

    # Configure, pylint: disable=too-many-branches,too-many-locals,too-many-statements
    def configure(self, configurations: Dict[str, Any]) -> Dict[str, str]:

        # Variables
        result = {}

        # Header
        print(' ')
        print(
            f' {Colors.GREEN}===[ {Colors.YELLOW}Configurations menu' \
                f' {Colors.GREEN}]==={Colors.RESET}'
        )
        print(' ')
        Platform.flush()

        # Walk through configurations
        for variable in configurations:

            # Variables
            variable_choices = []
            variable_default = ''
            variable_index = 0
            variable_set = False
            variable_values = []

            # Extract configuration fields
            variable_node = configurations[variable]
            variable_help = variable_node['help']
            variable_type = variable_node['type']

            # Prepare configuration selection
            configuration_message = f'Variable {variable}: {variable_help}:'
            configuration_type = None

            # Extract environment variable
            if variable in environ:
                variable_default = environ[variable]
                variable_set = True

            # Parse configuration types: boolean
            if variable_type == 'boolean':
                if 'default' in variable_node and variable_node['default'] in [
                        False, 'false'
                ]:
                    variable_values = ['false', 'true']
                else:
                    variable_values = ['true', 'false']
                if not variable_set:
                    variable_default = variable_values[0]
                for choice in variable_values:
                    variable_index += 1
                    variable_choices += [{
                        # 'key': str(variable_index),
                        'name': f'{choice}',
                        'value': choice
                    }]
                configuration_type = 'select'

            # Parse configuration types: choice
            elif variable_type == 'choice':
                variable_values = variable_node['values']
                if not variable_set:
                    variable_default = variable_values[0]
                for choice in variable_values:
                    variable_index += 1
                    variable_choices += [{
                        'key': str(variable_index),
                        'name': f'{choice}',
                        'value': choice
                    }]
                configuration_type = 'select'

            # Parse configuration types: input
            elif variable_type == 'input':
                configuration_type = 'text'
                if 'default' in variable_node and variable_node[
                        'default'] and not variable_set:
                    variable_default = variable_node['default']

            # Parse configuration types: json
            elif variable_type == 'json':
                if not variable_set:
                    configuration_path = Path(self.__options.path) / variable_node['path']
                    configuration_key = variable_node['key']
                    with open(configuration_path, encoding='utf8',
                              mode='r') as configuration_data:
                        configuration_dict = json_load(configuration_data)
                        variable_values = Dicts.find(configuration_dict,
                                                     configuration_key)
                        if not variable_values:
                            raise ValueError(
                                f'Unknown "{configuration_key}" key in' \
                                    f' {configuration_path} for f"{variable}"'
                            )
                        if isinstance(variable_values, str):
                            variable_values = [variable_values]
                        for choice in variable_values:
                            variable_index += 1
                            variable_choices += [{
                                'key': str(variable_index),
                                'name': f'{choice}',
                                'value': choice
                            }]
                        configuration_type = 'select'
                        variable_default = variable_values[0]

            # Parse configuration types: yaml
            elif variable_type == 'yaml':
                if not variable_set:
                    configuration_path = Path(self.__options.path) / variable_node['path']
                    configuration_key = variable_node['key']
                    with open(configuration_path, encoding='utf8',
                              mode='r') as configuration_data:
                        configuration_dict = YAML.load(configuration_data)
                        variable_values = Dicts.find(configuration_dict,
                                                     configuration_key)
                        if not variable_values:
                            raise ValueError(
                                f'Unknown "{configuration_key}" key in' \
                                    f' {configuration_path} for f"{variable}"'
                            )
                        if isinstance(variable_values, str):
                            variable_values = [variable_values]
                        for choice in variable_values:
                            variable_index += 1
                            variable_choices += [{
                                'key': str(variable_index),
                                'name': f'{choice}',
                                'value': choice
                            }]
                        configuration_type = 'select'
                        variable_default = variable_values[0]

            # Parse configuration types: unknown
            else:
                print(' ')
                print(
                    f' {Colors.GREEN}{Bundle.NAME}: {Colors.RED}ERROR:' \
                        f' {Colors.BOLD}Unsupported configuration type ' \
                            f'"{variable_type}"...{Colors.RESET}'
                )
                print(' ')
                Platform.flush()
                raise NotImplementedError(
                    f'Unsupported configuration type "{variable_type}"')

            # Extract environment variable
            if variable in environ:
                variable_default = environ[variable]
                variable_set = True

            # Request configuration selection
            if not Platform.IS_TTY_STDIN or variable_set or self.__options.defaults:
                result[variable] = str(variable_default)
                print(
                    f' {Colors.YELLOW}{configuration_message}' \
                        f'  {Colors.CYAN}{result[variable]}{Colors.RESET}'
                )
            else:
                if configuration_type == 'select':
                    answers = questionary_select(
                        message=configuration_message,
                        choices=variable_choices,
                        qmark='',
                        pointer=Themes.POINTER,
                        style=Themes.configuration_style(),
                        use_indicator=False,
                        use_shortcuts=False,
                        use_arrow_keys=True,
                        use_jk_keys=True,
                        show_selected=False,
                    ).ask()
                elif configuration_type == 'text':
                    answers = questionary_text(
                        message=configuration_message,
                        default=variable_default,
                        qmark='',
                        style=Themes.configuration_style(),
                        multiline=False,
                    ).ask()
                else: # pragma: no cover
                    answers = None
                if not answers:
                    raise KeyboardInterrupt
                result[variable] = str(answers)

        # Footer
        print(' ')
        Platform.flush()

        # Result
        return result

    # Select, pylint: disable=too-many-branches,too-many-statements
    def select(self) -> bool:

        # Variables
        default_check: bool = self.__options.all
        jobs_available: bool = False
        jobs_choices: List[Union[questionary_Choice, questionary_Separator]] = []
        result: bool = True
        stage: str = ''

        # Stages groups
        for job in self.__jobs:

            # Filter names
            if self.__options.names:

                # Filter jobs list
                if not self.__options.pipeline and not Lists.match(
                        self.__options.names, job, ignore_case=self.__options.ignore_case,
                        no_regex=self.__options.no_regex):
                    continue

                # Filter stages list
                if self.__options.pipeline and not Lists.match(
                        self.__options.names, self.__jobs[job]['stage'],
                        ignore_case=self.__options.ignore_case,
                        no_regex=self.__options.no_regex):
                    continue

            # Stages separator
            if stage != self.__jobs[job]['stage']:
                stage = self.__jobs[job]['stage']
                jobs_choices += [questionary_Separator(f'\n Stage {stage}:')]

            # Initial job details
            job_details_list: List[str] = []
            job_details_string: str = ''

            # Disabled jobs
            disabled: Optional[str] = None
            if self.__jobs[job]['when'] in ['manual'] and not self.__options.manual:
                disabled = 'Manual'
            else:
                if self.__jobs[job]['when'] == 'manual':
                    job_details_list += ['Manual']
                elif self.__jobs[job]['when'] == 'on_failure':
                    job_details_list += ['On failure']
                jobs_available = True

            # Parser disabled jobs
            if self.__jobs[job]['options'].disabled:
                disabled = self.__jobs[job]['options'].disabled

            # Failure allowed jobs
            if self.__jobs[job]['allow_failure']:
                job_details_list += ['Failure allowed']

            # Register job tags
            tags = ''
            if self.__jobs[job]['tags']:
                tags = f" [{','.join(self.__jobs[job]['tags'])}]"

            # Prepare job details
            if job_details_list:
                job_details_string = f" ({', '.join(job_details_list)})"

            # Job choices
            jobs_choices += [
                questionary_Choice(
                    title=f"{self.__jobs[job]['name']}{tags}{job_details_string}",
                    value=job,
                    disabled=disabled,
                    checked=default_check,
                    shortcut_key=True,
                )
            ]

        # Request jobs selection
        if jobs_choices and jobs_available:
            if self.__options.list:
                answers = questionary_select(
                    message='===[ Jobs selector ]===',
                    choices=jobs_choices,
                    qmark='',
                    pointer=Themes.POINTER,
                    style=Themes.configuration_style(),
                    use_indicator=False,
                    use_shortcuts=False,
                    use_arrow_keys=True,
                    use_jk_keys=True,
                    show_selected=False,
                ).ask()
            else:
                answers = questionary_checkbox(
                    message='===[ Jobs selector ]===',
                    choices=jobs_choices,
                    qmark='',
                    pointer=Themes.POINTER,
                    style=Themes.checkbox_style(),
                    use_arrow_keys=True,
                    use_jk_keys=True,
                ).ask()

        # No jobs found
        else:
            print(
                f' {Colors.GREEN}{Bundle.NAME}: {Colors.RED}ERROR:' \
                    f' {Colors.BOLD}No jobs found for selection{Colors.RESET}'
            )
            answers = None

        # Parse jobs selection
        if answers:
            if self.__options.list:
                self.__options.names = [answers]
            else:
                self.__options.names = answers
        else:
            self.__options.names = []

        # Drop pipeline mode for jobs
        self.__options.pipeline = False

        # Footer
        print(' ')
        print(' ')
        Platform.flush()

        # Launch jobs
        if self.__options.names:
            result = PipelinesFeature(self.__jobs, self.__options).launch()

        # Result
        return result
