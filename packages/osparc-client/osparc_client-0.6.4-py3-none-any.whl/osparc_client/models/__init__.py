# coding: utf-8

# flake8: noqa
"""
    osparc.io web API (dev)

    osparc-simcore public API specifications  # noqa: E501

    The version of the OpenAPI document: 0.5.0-dev
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

# import models into model package
from osparc_client.models.body_abort_multipart_upload_v0_files_file_id_abort_post import BodyAbortMultipartUploadV0FilesFileIdAbortPost
from osparc_client.models.body_complete_multipart_upload_v0_files_file_id_complete_post import BodyCompleteMultipartUploadV0FilesFileIdCompletePost
from osparc_client.models.body_upload_file_v0_files_content_put import BodyUploadFileV0FilesContentPut
from osparc_client.models.client_file import ClientFile
from osparc_client.models.client_file_upload_data import ClientFileUploadData
from osparc_client.models.error_get import ErrorGet
from osparc_client.models.file import File
from osparc_client.models.file_upload_completion_body import FileUploadCompletionBody
from osparc_client.models.file_upload_data import FileUploadData
from osparc_client.models.groups import Groups
from osparc_client.models.http_validation_error import HTTPValidationError
from osparc_client.models.job import Job
from osparc_client.models.job_inputs import JobInputs
from osparc_client.models.job_metadata import JobMetadata
from osparc_client.models.job_metadata_update import JobMetadataUpdate
from osparc_client.models.job_outputs import JobOutputs
from osparc_client.models.job_status import JobStatus
from osparc_client.models.links import Links
from osparc_client.models.meta import Meta
from osparc_client.models.one_page_solver_port import OnePageSolverPort
from osparc_client.models.one_page_study_port import OnePageStudyPort
from osparc_client.models.page_file import PageFile
from osparc_client.models.page_job import PageJob
from osparc_client.models.page_solver import PageSolver
from osparc_client.models.page_study import PageStudy
from osparc_client.models.pricing_plan_classification import PricingPlanClassification
from osparc_client.models.pricing_unit_get import PricingUnitGet
from osparc_client.models.profile import Profile
from osparc_client.models.profile_update import ProfileUpdate
from osparc_client.models.running_state import RunningState
from osparc_client.models.service_pricing_plan_get import ServicePricingPlanGet
from osparc_client.models.solver import Solver
from osparc_client.models.solver_port import SolverPort
from osparc_client.models.study import Study
from osparc_client.models.study_port import StudyPort
from osparc_client.models.upload_links import UploadLinks
from osparc_client.models.uploaded_part import UploadedPart
from osparc_client.models.user_role_enum import UserRoleEnum
from osparc_client.models.users_group import UsersGroup
from osparc_client.models.validation_error import ValidationError
from osparc_client.models.wallet_get_with_available_credits import WalletGetWithAvailableCredits
from osparc_client.models.wallet_status import WalletStatus
