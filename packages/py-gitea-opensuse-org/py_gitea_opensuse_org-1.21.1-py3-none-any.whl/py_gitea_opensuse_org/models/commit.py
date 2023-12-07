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

from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional
from pydantic import BaseModel, StrictStr
from py_gitea_opensuse_org.models.commit_affected_files import CommitAffectedFiles
from py_gitea_opensuse_org.models.commit_meta import CommitMeta
from py_gitea_opensuse_org.models.commit_stats import CommitStats
from py_gitea_opensuse_org.models.repo_commit import RepoCommit
from py_gitea_opensuse_org.models.user import User
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class Commit(BaseModel):
    """
    Commit
    """ # noqa: E501
    author: Optional[User] = None
    commit: Optional[RepoCommit] = None
    committer: Optional[User] = None
    created: Optional[datetime] = None
    files: Optional[List[CommitAffectedFiles]] = None
    html_url: Optional[StrictStr] = None
    parents: Optional[List[CommitMeta]] = None
    sha: Optional[StrictStr] = None
    stats: Optional[CommitStats] = None
    url: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["author", "commit", "committer", "created", "files", "html_url", "parents", "sha", "stats", "url"]

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
        """Create an instance of Commit from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of author
        if self.author:
            _dict['author'] = self.author.to_dict()
        # override the default output from pydantic by calling `to_dict()` of commit
        if self.commit:
            _dict['commit'] = self.commit.to_dict()
        # override the default output from pydantic by calling `to_dict()` of committer
        if self.committer:
            _dict['committer'] = self.committer.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in files (list)
        _items = []
        if self.files:
            for _item in self.files:
                if _item:
                    _items.append(_item.to_dict())
            _dict['files'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in parents (list)
        _items = []
        if self.parents:
            for _item in self.parents:
                if _item:
                    _items.append(_item.to_dict())
            _dict['parents'] = _items
        # override the default output from pydantic by calling `to_dict()` of stats
        if self.stats:
            _dict['stats'] = self.stats.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of Commit from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "author": User.from_dict(obj.get("author")) if obj.get("author") is not None else None,
            "commit": RepoCommit.from_dict(obj.get("commit")) if obj.get("commit") is not None else None,
            "committer": User.from_dict(obj.get("committer")) if obj.get("committer") is not None else None,
            "created": obj.get("created"),
            "files": [CommitAffectedFiles.from_dict(_item) for _item in obj.get("files")] if obj.get("files") is not None else None,
            "html_url": obj.get("html_url"),
            "parents": [CommitMeta.from_dict(_item) for _item in obj.get("parents")] if obj.get("parents") is not None else None,
            "sha": obj.get("sha"),
            "stats": CommitStats.from_dict(obj.get("stats")) if obj.get("stats") is not None else None,
            "url": obj.get("url")
        })
        return _obj


