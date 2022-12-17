from __future__ import annotations

import base64
import io
from typing import List, Optional

from companycam.manager import BaseManager
from companycam.manager import delete as delete_
from companycam.manager import get, post, put, request
from companycam.types import QueryParamTypes
from companycam.v2.models import (
    Comment,
    Company,
    Coordinate,
    Document,
    Group,
    Photo,
    Project,
    ProjectCollaborator,
    ProjectInvitation,
    ProjectNotepad,
    Tag,
    User,
    Webhook,
)

QueryTypes = Optional[QueryParamTypes]


class CompanyManager(BaseManager):
    @get("/company", Company)
    def retrieve(self) -> Company:
        return request()


class UsersManager(BaseManager):
    # this is defined here, rather than in `pydantic.BaseModel.Config`, and applied
    # manually so it's closer to the path definitions and not invoked in any non-API
    # usage of `BaseModel.dict()`
    include = {"first_name", "last_name", "email_address", "phone_number", "password"}

    @get("/users/current", User)
    def retrieve_current(self) -> User:
        return request()

    @get("/users", List[User])
    def list(self, query: QueryTypes = None) -> List[User]:
        return request(params=query)

    @post("/users", User)
    def create(self, user: User) -> User:
        return request(json=user.dict(include=self.include))

    @get("/users/{user}", User)
    def retrieve(self, user: User | str) -> User:
        return request()

    @put("/users/{user}", User)
    def update(self, user: User) -> User:
        return request(json=user.dict(include=self.include))

    @delete_("/users/{user}", bool)
    def delete(self, user: User | str) -> bool:
        return request()


class ProjectsManager(BaseManager):
    include = {"name", "address", "coordinates", "geofence", "primary_contact"}

    @get("/projects", List[Project])
    def list(self, query: QueryTypes = None) -> List[Project]:
        return request(params=query)

    @post("/projects", Project)
    def create(self, project: Project) -> Project:
        return request(json=project.dict(include=self.include))

    @get("/projects/{project}", Project)
    def retrieve(self, project: Project | str) -> Project:
        return request()

    @put("/projects/{project}", Project)
    def update(self, project: Project) -> Project:
        include = self.include.copy()
        include.remove("primary_contact")
        return request(json=project.dict(include=include))

    @delete_("/projects/{project}", bool)
    def delete(self, project: Project | str) -> bool:
        return request()

    @put("/projects/{project}/restore", Project)
    def restore(self, project: Project | str) -> Project:
        return request()

    @get("/projects/{project}/photos", List[Photo])
    def list_photos(
        self, project: Project | str, query: QueryTypes = None
    ) -> List[Photo]:
        return request(params=query)

    @post("/projects/{project}/photos", Photo)
    def create_photo(
        self,
        project: Project | str,
        uri: str,
        captured_at: int,
        coordinates: Optional[Coordinate] = None,
    ) -> Photo:
        photo_dict = {"captured_at": captured_at, "uri": uri}
        if coordinates:
            photo_dict["coordinates"] = coordinates.dict()
        return request(json={"photo": photo_dict})

    @get("/projects/{project}/assigned_users", List[User])
    def list_assigned_users(
        self, project: Project | str, query: QueryTypes = None
    ) -> List[User]:
        return request(params=query)

    @put("/projects/{project}/assigned_users/{user}", User)
    def assign_user_to_project(self, project: Project | str, user: User | str) -> User:
        return request()

    @delete_("/projects/{project}/assigned_users/{user}", bool)
    def remove_user_from_project(
        self, project: Project | str, user: User | str
    ) -> bool:
        return request()

    @put("/projects/{project}/notepad", ProjectNotepad)
    def update_notepad(self, project: Project) -> ProjectNotepad:
        return request(json=project.dict(include={"notepad"}))

    @get("/projects/{project}/collaborators", List[ProjectCollaborator])
    def list_collaborators(
        self, project: Project | str, query: QueryTypes = None
    ) -> List[ProjectCollaborator]:
        return request(params=query)

    @get("/projects/{project}/invitations", List[ProjectInvitation])
    def list_invitations(
        self, project: Project | str, query: QueryTypes = None
    ) -> List[ProjectInvitation]:
        return request(params=query)

    @post("/projects/{project}/invitations", ProjectInvitation)
    def create_invitation(
        self, project: Project | str, invitation: ProjectInvitation
    ) -> ProjectInvitation:
        return request(json=invitation.dict(include={"permissions"}))

    @get("/projects/{project}/labels", List[Tag])
    def list_labels(
        self, project: Project | str, query: QueryTypes = None
    ) -> List[Tag]:
        return request(params=query)

    @post("/projects/{project}/labels", List[Tag])
    def create_labels(self, project: Project | str, *labels: str) -> List[Tag]:
        return request(json={"project": {"labels": [*labels]}})

    @delete_("/projects/{project}/labels/{label}", bool)
    def delete_label(self, project: Project | str, label: Tag | str) -> bool:
        return request()

    @get("/projects/{project}/documents", List[Document])
    def list_documents(
        self, project: Project | str, query: QueryTypes = None
    ) -> List[Document]:
        return request(params=query)

    @post("/projects/{project}/documents", Document)
    def create_document(
        self, project: Project | str, file: io.BufferedReader, encoding: str = "utf-8"
    ) -> Document:
        document = {
            "name": file.name,
            "attachment": base64.b64encode(file.read()).decode(encoding),
        }
        return request(json={"document": document})

    @get("/projects/{project}/comments", List[Comment])
    def list_comments(
        self, project: Project | str, query: QueryTypes = None
    ) -> List[Comment]:
        return request(params=query)

    @post("/projects/{project}/comments", Comment)
    def create_comment(self, project: Project | str, comment: Comment) -> Comment:
        return request(json={"comment": comment.dict(include={"content"})})


class PhotosManager(BaseManager):
    @get("/photos", List[Photo])
    def list(self, query: QueryTypes = None) -> List[Photo]:
        return request(params=query)

    @get("/photos/{photo}", Photo)
    def retrieve(self, photo: Photo | str) -> Photo:
        return request()

    @put("/photos/{photo}", Photo)
    def update(self, photo: Photo) -> Photo:
        return request(json={"photo": photo.dict(include={"internal"})})

    @delete_("/photos/{photo}", bool)
    def delete(self, photo: Photo | str) -> bool:
        return request()

    @get("/photos/{photo}/tags", List[Tag])
    def list_tags(self, photo: Photo | str, query: QueryTypes = None) -> List[Tag]:
        return request(params=query)

    @post("/photos/{photo}/tags", List[Tag])
    def create_tags(self, photo: Photo | str, *tags: str) -> List[Tag]:
        return request(json={"tags": [*tags]})

    @get("/photos/{photo}/comments", List[Comment])
    def list_comments(
        self, photo: Photo | str, query: QueryTypes = None
    ) -> List[Comment]:
        return request(params=query)

    @post("/photos/{photo}/comments", Comment)
    def create_comment(self, photo: Photo | str, comment: Comment) -> Comment:
        return request(json={"comment": comment.dict(include={"content"})})


class TagsManager(BaseManager):
    @get("/tags", List[Tag])
    def list(self, query: QueryTypes = None) -> List[Tag]:
        return request(params=query)

    @post("/tags", Tag)
    def create(self, tag: Tag) -> Tag:
        return request(json={"tag": tag.dict(include={"display_value"})})

    @get("/tags/{tag}", Tag)
    def retrieve(self, tag: Tag | str) -> Tag:
        return request()

    @put("/tags/{tag}", Tag)
    def update(self, tag: Tag) -> Tag:
        return request(json={"tag": tag.dict(include={"display_value"})})

    @delete_("/tags/{tag}", bool)
    def delete(self, tag: Tag | str) -> bool:
        return request()


class GroupsManager(BaseManager):
    @get("/groups", List[Group])
    def list(self, query: QueryTypes = None) -> List[Group]:
        return request(params=query)

    @post("/groups", Group)
    def create(self, group: Group) -> Group:
        group_dict = group.dict(include={"name", "users"})
        if users := group_dict.pop("users", None):
            group_dict["users"] = [u["id"] for u in users if "id" in u]
        return request(json={"group": group_dict})

    @get("/groups/{group}", Group)
    def retrieve(self, group: Group | str) -> Group:
        return request()

    @put("/groups/{group}", Group)
    def update(self, group: Group) -> Group:
        group_dict = group.dict(include={"name", "users"})
        if users := group_dict.pop("users", None):
            group_dict["users"] = [u["id"] for u in users if "id" in u]
        return request(json={"group": group_dict})

    @delete_("/groups/{group}", bool)
    def delete(self, group: Group | str) -> bool:
        return request()


class WebhooksManager(BaseManager):
    @get("/webhooks", List[Webhook])
    def list(self, query: QueryTypes = None) -> List[Webhook]:
        return request(params=query)

    @post("/webhooks", Webhook)
    def create(self, webhook: Webhook) -> Webhook:
        return request(json=webhook.dict(include={"url", "scopes", "enabled", "token"}))

    @get("/webhooks/{webhook}", Webhook)
    def retrieve(self, webhook: Webhook | str) -> Webhook:
        return request()

    @put("/webhooks/{webhook}", Webhook)
    def update(self, webhook: Webhook) -> Webhook:
        return request(json=webhook.dict(include={"url", "scopes", "enabled", "token"}))

    @delete_("/webhooks/{webhook}", bool)
    def delete(self, webhook: Webhook | str) -> bool:
        return request()
