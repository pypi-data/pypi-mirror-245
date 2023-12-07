# coding: utf-8

"""
    Gitea API

    This documentation describes the Gitea API.

    The version of the OpenAPI document: 1.21.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, ClassVar, Dict, List, Optional
from pydantic import BaseModel, StrictBool, StrictStr
from pydantic import Field
from py_gitea_opensuse_org.models.external_tracker import ExternalTracker
from py_gitea_opensuse_org.models.external_wiki import ExternalWiki
from py_gitea_opensuse_org.models.internal_tracker import InternalTracker
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class EditRepoOption(BaseModel):
    """
    EditRepoOption options when editing a repository's properties
    """ # noqa: E501
    allow_manual_merge: Optional[StrictBool] = Field(default=None, description="either `true` to allow mark pr as merged manually, or `false` to prevent it.")
    allow_merge_commits: Optional[StrictBool] = Field(default=None, description="either `true` to allow merging pull requests with a merge commit, or `false` to prevent merging pull requests with merge commits.")
    allow_rebase: Optional[StrictBool] = Field(default=None, description="either `true` to allow rebase-merging pull requests, or `false` to prevent rebase-merging.")
    allow_rebase_explicit: Optional[StrictBool] = Field(default=None, description="either `true` to allow rebase with explicit merge commits (--no-ff), or `false` to prevent rebase with explicit merge commits.")
    allow_rebase_update: Optional[StrictBool] = Field(default=None, description="either `true` to allow updating pull request branch by rebase, or `false` to prevent it.")
    allow_squash_merge: Optional[StrictBool] = Field(default=None, description="either `true` to allow squash-merging pull requests, or `false` to prevent squash-merging.")
    archived: Optional[StrictBool] = Field(default=None, description="set to `true` to archive this repository.")
    autodetect_manual_merge: Optional[StrictBool] = Field(default=None, description="either `true` to enable AutodetectManualMerge, or `false` to prevent it. Note: In some special cases, misjudgments can occur.")
    default_allow_maintainer_edit: Optional[StrictBool] = Field(default=None, description="set to `true` to allow edits from maintainers by default")
    default_branch: Optional[StrictStr] = Field(default=None, description="sets the default branch for this repository.")
    default_delete_branch_after_merge: Optional[StrictBool] = Field(default=None, description="set to `true` to delete pr branch after merge by default")
    default_merge_style: Optional[StrictStr] = Field(default=None, description="set to a merge style to be used by this repository: \"merge\", \"rebase\", \"rebase-merge\", or \"squash\".")
    description: Optional[StrictStr] = Field(default=None, description="a short description of the repository.")
    enable_prune: Optional[StrictBool] = Field(default=None, description="enable prune - remove obsolete remote-tracking references")
    external_tracker: Optional[ExternalTracker] = None
    external_wiki: Optional[ExternalWiki] = None
    has_actions: Optional[StrictBool] = Field(default=None, description="either `true` to enable actions unit, or `false` to disable them.")
    has_issues: Optional[StrictBool] = Field(default=None, description="either `true` to enable issues for this repository or `false` to disable them.")
    has_packages: Optional[StrictBool] = Field(default=None, description="either `true` to enable packages unit, or `false` to disable them.")
    has_projects: Optional[StrictBool] = Field(default=None, description="either `true` to enable project unit, or `false` to disable them.")
    has_pull_requests: Optional[StrictBool] = Field(default=None, description="either `true` to allow pull requests, or `false` to prevent pull request.")
    has_releases: Optional[StrictBool] = Field(default=None, description="either `true` to enable releases unit, or `false` to disable them.")
    has_wiki: Optional[StrictBool] = Field(default=None, description="either `true` to enable the wiki for this repository or `false` to disable it.")
    ignore_whitespace_conflicts: Optional[StrictBool] = Field(default=None, description="either `true` to ignore whitespace for conflicts, or `false` to not ignore whitespace.")
    internal_tracker: Optional[InternalTracker] = None
    mirror_interval: Optional[StrictStr] = Field(default=None, description="set to a string like `8h30m0s` to set the mirror interval time")
    name: Optional[StrictStr] = Field(default=None, description="name of the repository")
    private: Optional[StrictBool] = Field(default=None, description="either `true` to make the repository private or `false` to make it public. Note: you will get a 422 error if the organization restricts changing repository visibility to organization owners and a non-owner tries to change the value of private.")
    template: Optional[StrictBool] = Field(default=None, description="either `true` to make this repository a template or `false` to make it a normal repository")
    website: Optional[StrictStr] = Field(default=None, description="a URL with more information about the repository.")
    __properties: ClassVar[List[str]] = ["allow_manual_merge", "allow_merge_commits", "allow_rebase", "allow_rebase_explicit", "allow_rebase_update", "allow_squash_merge", "archived", "autodetect_manual_merge", "default_allow_maintainer_edit", "default_branch", "default_delete_branch_after_merge", "default_merge_style", "description", "enable_prune", "external_tracker", "external_wiki", "has_actions", "has_issues", "has_packages", "has_projects", "has_pull_requests", "has_releases", "has_wiki", "ignore_whitespace_conflicts", "internal_tracker", "mirror_interval", "name", "private", "template", "website"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of EditRepoOption from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of external_tracker
        if self.external_tracker:
            _dict['external_tracker'] = self.external_tracker.to_dict()
        # override the default output from pydantic by calling `to_dict()` of external_wiki
        if self.external_wiki:
            _dict['external_wiki'] = self.external_wiki.to_dict()
        # override the default output from pydantic by calling `to_dict()` of internal_tracker
        if self.internal_tracker:
            _dict['internal_tracker'] = self.internal_tracker.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of EditRepoOption from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "allow_manual_merge": obj.get("allow_manual_merge"),
            "allow_merge_commits": obj.get("allow_merge_commits"),
            "allow_rebase": obj.get("allow_rebase"),
            "allow_rebase_explicit": obj.get("allow_rebase_explicit"),
            "allow_rebase_update": obj.get("allow_rebase_update"),
            "allow_squash_merge": obj.get("allow_squash_merge"),
            "archived": obj.get("archived"),
            "autodetect_manual_merge": obj.get("autodetect_manual_merge"),
            "default_allow_maintainer_edit": obj.get("default_allow_maintainer_edit"),
            "default_branch": obj.get("default_branch"),
            "default_delete_branch_after_merge": obj.get("default_delete_branch_after_merge"),
            "default_merge_style": obj.get("default_merge_style"),
            "description": obj.get("description"),
            "enable_prune": obj.get("enable_prune"),
            "external_tracker": ExternalTracker.from_dict(obj.get("external_tracker")) if obj.get("external_tracker") is not None else None,
            "external_wiki": ExternalWiki.from_dict(obj.get("external_wiki")) if obj.get("external_wiki") is not None else None,
            "has_actions": obj.get("has_actions"),
            "has_issues": obj.get("has_issues"),
            "has_packages": obj.get("has_packages"),
            "has_projects": obj.get("has_projects"),
            "has_pull_requests": obj.get("has_pull_requests"),
            "has_releases": obj.get("has_releases"),
            "has_wiki": obj.get("has_wiki"),
            "ignore_whitespace_conflicts": obj.get("ignore_whitespace_conflicts"),
            "internal_tracker": InternalTracker.from_dict(obj.get("internal_tracker")) if obj.get("internal_tracker") is not None else None,
            "mirror_interval": obj.get("mirror_interval"),
            "name": obj.get("name"),
            "private": obj.get("private"),
            "template": obj.get("template"),
            "website": obj.get("website")
        })
        return _obj


