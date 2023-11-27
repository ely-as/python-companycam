import base64
import io

from companycam.manager import BaseManager, get, post, put, request
from companycam.manager import delete as delete_
from companycam.types import QueryParamTypes
from companycam.utils import model_dump
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

QueryTypes = QueryParamTypes | None


class CompanyManager(BaseManager):
    @get("/company")
    def retrieve(self) -> Company:
        return request()


class UsersManager(BaseManager):
    # this is defined here, rather than in `pydantic.BaseModel.Config`, and applied
    # manually so it's closer to the path definitions and not invoked in any non-API
    # usage of `BaseModel.model_dump()` (formerly `BaseModel.dict()`)
    include = {"first_name", "last_name", "email_address", "phone_number", "password"}

    @get("/users/current")
    def retrieve_current(self) -> User:
        return request()

    @get("/users")
    def list(self, query: QueryTypes = None) -> list[User]:
        return request(params=query)

    @post("/users")
    def create(self, user: User) -> User:
        return request(json=model_dump(user, include=self.include))

    @get("/users/{user}")
    def retrieve(self, user: User | str) -> User:
        return request()

    @put("/users/{user}")
    def update(self, user: User) -> User:
        return request(json=model_dump(user, include=self.include))

    @delete_("/users/{user}")
    def delete(self, user: User | str) -> bool:
        return request()


class ProjectsManager(BaseManager):
    include = {"name", "address", "coordinates", "geofence", "primary_contact"}

    @post("/projects")
    def create(self, project: Project) -> Project:
        return request(json=model_dump(project, include=self.include))

    @get("/projects/{project}")
    def retrieve(self, project: Project | str) -> Project:
        return request()

    @put("/projects/{project}")
    def update(self, project: Project) -> Project:
        include = self.include.copy()
        include.remove("primary_contact")
        return request(json=model_dump(project, include=include))

    @delete_("/projects/{project}")
    def delete(self, project: Project | str) -> bool:
        return request()

    @put("/projects/{project}/restore")
    def restore(self, project: Project | str) -> Project:
        return request()

    @get("/projects/{project}/photos")
    def list_photos(
        self, project: Project | str, query: QueryTypes = None
    ) -> list[Photo]:
        return request(params=query)

    @post("/projects/{project}/photos")
    def create_photo(
        self,
        project: Project | str,
        uri: str,
        captured_at: int,
        coordinates: Coordinate | None = None,
    ) -> Photo:
        photo_dict = {"captured_at": captured_at, "uri": uri}
        if coordinates:
            photo_dict["coordinates"] = model_dump(coordinates)
        return request(json={"photo": photo_dict})

    @get("/projects/{project}/assigned_users")
    def list_assigned_users(
        self, project: Project | str, query: QueryTypes = None
    ) -> list[User]:
        return request(params=query)

    @put("/projects/{project}/assigned_users/{user}")
    def assign_user_to_project(self, project: Project | str, user: User | str) -> User:
        return request()

    @delete_("/projects/{project}/assigned_users/{user}")
    def remove_user_from_project(
        self, project: Project | str, user: User | str
    ) -> bool:
        return request()

    @put("/projects/{project}/notepad")
    def update_notepad(self, project: Project) -> ProjectNotepad:
        return request(json=model_dump(project, include={"notepad"}))

    @get("/projects/{project}/collaborators")
    def list_collaborators(
        self, project: Project | str, query: QueryTypes = None
    ) -> list[ProjectCollaborator]:
        return request(params=query)

    @get("/projects/{project}/invitations")
    def list_invitations(
        self, project: Project | str, query: QueryTypes = None
    ) -> list[ProjectInvitation]:
        return request(params=query)

    @post("/projects/{project}/invitations")
    def create_invitation(self, project: Project | str) -> ProjectInvitation:
        return request()

    @get("/projects/{project}/labels")
    def list_labels(
        self, project: Project | str, query: QueryTypes = None
    ) -> list[Tag]:
        return request(params=query)

    @post("/projects/{project}/labels")
    def create_labels(self, project: Project | str, *labels: str) -> list[Tag]:
        return request(json={"project": {"labels": [*labels]}})

    @delete_("/projects/{project}/labels/{label}")
    def delete_label(self, project: Project | str, label: Tag | str) -> bool:
        return request()

    @get("/projects/{project}/documents")
    def list_documents(
        self, project: Project | str, query: QueryTypes = None
    ) -> list[Document]:
        return request(params=query)

    @post("/projects/{project}/documents")
    def create_document(
        self, project: Project | str, file: io.BufferedReader, encoding: str = "utf-8"
    ) -> Document:
        document = {
            "name": file.name,
            "attachment": base64.b64encode(file.read()).decode(encoding),
        }
        return request(json={"document": document})

    @get("/projects/{project}/comments")
    def list_comments(
        self, project: Project | str, query: QueryTypes = None
    ) -> list[Comment]:
        return request(params=query)

    @post("/projects/{project}/comments")
    def create_comment(self, project: Project | str, comment: Comment) -> Comment:
        return request(json={"comment": model_dump(comment, include={"content"})})

    @get("/projects")
    def list(self, query: QueryTypes = None) -> list[Project]:
        return request(params=query)


class PhotosManager(BaseManager):
    @get("/photos/{photo}")
    def retrieve(self, photo: Photo | str) -> Photo:
        return request()

    @put("/photos/{photo}")
    def update(self, photo: Photo) -> Photo:
        return request(json={"photo": model_dump(photo, include={"internal"})})

    @delete_("/photos/{photo}")
    def delete(self, photo: Photo | str) -> bool:
        return request()

    @get("/photos/{photo}/tags")
    def list_tags(self, photo: Photo | str, query: QueryTypes = None) -> list[Tag]:
        return request(params=query)

    @post("/photos/{photo}/tags")
    def create_tags(self, photo: Photo | str, *tags: str) -> list[Tag]:
        return request(json={"tags": [*tags]})

    @get("/photos/{photo}/comments")
    def list_comments(
        self, photo: Photo | str, query: QueryTypes = None
    ) -> list[Comment]:
        return request(params=query)

    @post("/photos/{photo}/comments")
    def create_comment(self, photo: Photo | str, comment: Comment) -> Comment:
        return request(json={"comment": model_dump(comment, include={"content"})})

    @get("/photos")
    def list(self, query: QueryTypes = None) -> list[Photo]:
        return request(params=query)


class TagsManager(BaseManager):
    @post("/tags")
    def create(self, tag: Tag) -> Tag:
        return request(json={"tag": model_dump(tag, include={"display_value"})})

    @get("/tags/{tag}")
    def retrieve(self, tag: Tag | str) -> Tag:
        return request()

    @put("/tags/{tag}")
    def update(self, tag: Tag) -> Tag:
        return request(json={"tag": model_dump(tag, include={"display_value"})})

    @delete_("/tags/{tag}")
    def delete(self, tag: Tag | str) -> bool:
        return request()

    @get("/tags")
    def list(self, query: QueryTypes = None) -> list[Tag]:
        return request(params=query)


class GroupsManager(BaseManager):
    @post("/groups")
    def create(self, group: Group) -> Group:
        group_dict = model_dump(group, include={"name", "users"})
        if users := group_dict.pop("users", None):
            group_dict["users"] = [u["id"] for u in users if "id" in u]
        return request(json={"group": group_dict})

    @get("/groups/{group}")
    def retrieve(self, group: Group | str) -> Group:
        return request()

    @put("/groups/{group}")
    def update(self, group: Group) -> Group:
        group_dict = model_dump(group, include={"name", "users"})
        if users := group_dict.pop("users", None):
            group_dict["users"] = [u["id"] for u in users if "id" in u]
        return request(json={"group": group_dict})

    @delete_("/groups/{group}")
    def delete(self, group: Group | str) -> bool:
        return request()

    @get("/groups")
    def list(self, query: QueryTypes = None) -> list[Group]:
        return request(params=query)


class WebhooksManager(BaseManager):
    @post("/webhooks")
    def create(self, webhook: Webhook) -> Webhook:
        return request(
            json=model_dump(webhook, include={"url", "scopes", "enabled", "token"})
        )

    @get("/webhooks/{webhook}")
    def retrieve(self, webhook: Webhook | str) -> Webhook:
        return request()

    @put("/webhooks/{webhook}")
    def update(self, webhook: Webhook) -> Webhook:
        return request(
            json=model_dump(webhook, include={"url", "scopes", "enabled", "token"})
        )

    @delete_("/webhooks/{webhook}")
    def delete(self, webhook: Webhook | str) -> bool:
        return request()

    @get("/webhooks")
    def list(self, query: QueryTypes = None) -> list[Webhook]:
        return request(params=query)
