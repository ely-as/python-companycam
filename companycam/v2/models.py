from typing import Literal

import pydantic
from typing_extensions import Annotated

from companycam.models import Model, ModelWithRequiredID
from companycam.utils import PYDANTIC_VERSION

if PYDANTIC_VERSION >= (2, 0, 0):
    OptionalInt = Annotated[int | None, pydantic.Field(default=None)]
    OptionalStr = Annotated[str | None, pydantic.Field(default=None)]
else:
    OptionalInt = int | None  # type: ignore[misc]
    OptionalStr = str | None  # type: ignore[misc]


# Components which don't reference other components, alphabetical


class Address(Model):
    street_address_1: OptionalStr
    street_address_2: OptionalStr
    city: OptionalStr
    state: OptionalStr
    postal_code: OptionalStr
    country: OptionalStr


class Comment(ModelWithRequiredID):
    creator_id: OptionalStr
    creator_type: OptionalStr
    creator_name: OptionalStr
    commentable_id: OptionalStr
    commentable_type: OptionalStr
    status: OptionalStr
    content: OptionalStr
    created_at: OptionalInt
    updated_at: OptionalInt


class Coordinate(Model):
    lat: float
    lon: float


class Document(ModelWithRequiredID):
    creator_id: OptionalStr
    creator_type: OptionalStr
    creator_name: OptionalStr
    project_id: OptionalStr
    name: OptionalStr
    url: OptionalStr
    content_type: OptionalStr
    byte_size: OptionalInt
    created_at: OptionalInt
    updated_at: OptionalInt


class Error(Model):
    errors: list[str] | None = None


class ImageURI(Model):
    type: str
    uri: str

    class Config:
        assignment_aliases = {"url": "uri"}


class ProjectCollaborator(Model):
    id: OptionalStr
    company_id: OptionalStr
    project_id: OptionalStr
    project_invitation_id: OptionalStr
    accepted_at: OptionalInt
    created_at: OptionalInt
    updated_at: OptionalInt


class ProjectContactRequest(Model):
    name: str
    email: OptionalStr
    phone_number: OptionalStr


class ProjectContactResponse(Model):
    id: OptionalStr
    project_id: OptionalStr
    name: OptionalStr
    email: OptionalStr
    phone_number: OptionalStr
    created_at: OptionalInt
    updated_at: OptionalInt


class ProjectInvitation(Model):
    id: OptionalStr
    project_id: OptionalStr
    invite_url: OptionalStr
    status: Literal["accepted", "expired", "pending"] | None = None
    accepted_at: OptionalInt
    accepted_by_id: OptionalStr
    expires_at: OptionalInt
    creator_id: OptionalStr
    created_at: OptionalInt
    updated_at: OptionalInt


class ProjectIntegration(Model):
    type: str
    relation_id: str


class ProjectNotepad(Model):
    notepad: str


class Tag(ModelWithRequiredID):
    company_id: OptionalStr
    display_value: OptionalStr
    value: OptionalStr
    created_at: OptionalInt
    updated_at: OptionalInt


class Webhook(ModelWithRequiredID):
    company_id: OptionalStr
    url: OptionalStr
    scopes: list[str] | None = None
    token: OptionalStr
    enabled: bool | None = None
    created_at: OptionalInt
    updated_at: OptionalInt


# Components which reference other components, alphabetical


class User(ModelWithRequiredID):
    company_id: OptionalStr
    email_address: OptionalStr
    status: Literal["active", "deleted"] | None = None
    first_name: OptionalStr
    last_name: OptionalStr
    profile_image: list[ImageURI] | None = None
    phone_number: OptionalStr
    created_at: OptionalInt
    updated_at: OptionalInt
    user_url: OptionalStr


# Rest of the components which reference other components, alphabetical


class Company(ModelWithRequiredID):
    name: str
    status: Literal["active", "cancelled", "deleted"] | None = None
    address: Address | None = None
    logo: list[ImageURI] | None = None


class Group(ModelWithRequiredID):
    company_id: OptionalStr
    name: OptionalStr
    users: list[User] | None = None
    status: Literal["active", "deleted"] | None = None
    group_url: OptionalStr
    created_at: OptionalInt
    updated_at: OptionalInt


class Photo(ModelWithRequiredID):
    company_id: OptionalStr
    creator_id: OptionalStr
    creator_type: OptionalStr
    creator_name: OptionalStr
    project_id: OptionalStr
    processing_status: Literal["pending", "processing", "processed", "processing_error", "duplicate"] | None = None  # fmt: skip
    coordinates: list[Coordinate] | None = None
    urls: list[ImageURI] | None = None
    hash: OptionalStr
    internal: bool | None = None
    photo_url: OptionalStr
    captured_at: OptionalInt
    created_at: OptionalInt
    updated_at: OptionalInt

    class Config:
        assignment_aliases = {"uris": "urls"}

    def __init__(self, *args, **kwargs) -> None:
        # Coerce `coordinates` to a list if dict is received in HTTP response
        if coordinates := kwargs.get("coordinates"):
            if isinstance(coordinates, dict):
                kwargs["coordinates"] = [coordinates]
        super().__init__(*args, **kwargs)


class Project(ModelWithRequiredID):
    company_id: OptionalStr
    creator_id: OptionalStr
    creator_type: OptionalStr
    creator_name: OptionalStr
    status: Literal["active", "deleted"] | None = None
    name: OptionalStr
    address: Address | None = None
    coordinates: Coordinate | None = None
    featured_image: list[ImageURI] | None = None
    project_url: OptionalStr
    embedded_project_url: OptionalStr
    integrations: list[ProjectIntegration] | None = None
    slug: OptionalStr
    public: bool | None = None
    geofence: list[Coordinate] | None = None
    primary_contact: ProjectContactResponse | None = None
    notepad: OptionalStr
    created_at: OptionalInt
    updated_at: OptionalInt
