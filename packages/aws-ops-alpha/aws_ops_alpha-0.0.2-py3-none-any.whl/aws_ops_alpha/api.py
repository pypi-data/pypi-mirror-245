# -*- coding: utf-8 -*-

"""
Usage example:

    >>> import aws_ops_alpha.api as aws_ops_alpha
    >>> aws_ops_alpha.runtime
    ...
    >>> aws_ops_alpha.get_devops_aws_account_id_in_ci()
    ...
    >>> aws_ops_alpha.get_workload_aws_account_id_in_ci("sbx")
    ...
"""

from . import constants
from .config import AwsOpsAlphaConfig as AwsOpsAlphaConfig
from .runtime import Runtime
from .runtime import RunTimeEnum
from .runtime import runtime
from .env_var import get_devops_aws_account_id_in_ci
from .env_var import get_workload_aws_account_id_in_ci
from .env_var import temp_env_var
from .environment import EnvEnum
from .environment import detect_current_env
from .git import InvalidSemanticNameError
from .git import SemanticBranchRule
from .git import GitRepo
from .git import MultiGitRepo
from .git import MonoGitRepo
from .boto_ses import BotoSesFactory
from .logger import logger
from . import constants
from .aws_helpers import aws_cdk_helpers
from .aws_helpers import aws_lambda_helpers

try:
    from .project.api import simple_python_project
    from .project.api import simple_cdk_project
    from .project.api import simple_lambda_project
except ImportError:
    pass
