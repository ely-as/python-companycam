from typing import Literal

from companycam.models import Model, ModelWithRequiredID

# Components which don't reference other components, alphabetical


class Address(Model):
    street_address_1: str | None
    street_address_2: str | None
    city: str | None
    state: str | None
    postal_code: str | None
    country: str | None


class Comment(ModelWithRequiredID):
    creator_id: str | None
    creator_type: str | None
    creator_name: str | None
    commentable_id: str | None
    commentable_type: str | None
    status: str | None
    content: str | None
    created_at: int | None
    updated_at: int | None


class Coordinate(Model):
    lat: float
    lon: float


class Document(ModelWithRequiredID):
    creator_id: str | None
    creator_type: str | None
    creator_name: str | None
    project_id: str | None
    name: str | None
    url: str | None
    content_type: str | None
    byte_size: int | None
    created_at: int | None
    updated_at: int | None


class Error(Model):
    errors: list[str] | None


class ImageURI(Model):
    type: str
    uri: str

    class Config:
        assignment_aliases = {"url": "uri"}


class ProjectCollaborator(Model):
    id: str | None
    company_id: str | None
    project_id: str | None
    project_invitation_id: str | None
    accepted_at: int | None
    created_at: int | None
    updated_at: int | None


class ProjectContactRequest(Model):
    name: str
    email: str | None
    phone_number: str | None


class ProjectContactResponse(Model):
    id: str | None
    project_id: str | None
    name: str | None
    email: str | None
    phone_number: str | None
    created_at: int | None
    updated_at: int | None


class ProjectInvitation(Model):
    id: str | None
    project_id: str | None
    invite_url: str | None
    status: Literal["accepted", "expired", "pending"] | None
    accepted_at: int | None
    accepted_by_id: str | None
    expires_at: int | None
    creator_id: str | None
    created_at: int | None
    updated_at: int | None


class ProjectIntegration(Model):
    type: str
    relation_id: str


class ProjectNotepad(Model):
    notepad: str


class Tag(ModelWithRequiredID):
    company_id: str | None
    display_value: str | None
    value: str | None
    created_at: int | None
    updated_at: int | None


class Webhook(ModelWithRequiredID):
    company_id: str | None
    url: str | None
    scopes: list[str] | None
    token: str | None
    enabled: bool | None
    created_at: int | None
    updated_at: int | None


# Components which reference other components, alphabetical


class User(ModelWithRequiredID):
    company_id: str | None
    email_address: str | None
    status: Literal["active", "deleted"] | None
    first_name: str | None
    last_name: str | None
    profile_image: list[ImageURI] | None
    phone_number: str | None
    created_at: int | None
    updated_at: int | None
    user_url: str | None


# Rest of the components which reference other components, alphabetical


class Company(ModelWithRequiredID):
    name: str
    status: Literal["active", "cancelled", "deleted"] | None
    address: Address | None
    logo: list[ImageURI] | None


class Group(ModelWithRequiredID):
    company_id: str | None
    name: str | None
    users: list[User] | None
    status: Literal["active", "deleted"] | None
    group_url: str | None
    created_at: int | None
    updated_at: int | None


class Photo(ModelWithRequiredID):
    company_id: str | None
    creator_id: str | None
    creator_type: str | None
    creator_name: str | None
    project_id: str | None
    processing_status: (
        Literal["pending", "processing", "processed", "processing_error", "duplicate"]
        | None
    )
    coordinates: list[Coordinate] | None
    urls: list[ImageURI] | None
    hash: str | None
    internal: bool | None
    photo_url: str | None
    captured_at: int | None
    created_at: int | None
    updated_at: int | None

    class Config:
        assignment_aliases = {"uris": "urls"}

    def __init__(self, *args, **kwargs) -> None:
        # Coerce `coordinates` to a list if dict is received in HTTP response
        if coordinates := kwargs.get("coordinates"):
            if isinstance(coordinates, dict):
                kwargs["coordinates"] = [coordinates]
        super().__init__(*args, **kwargs)


class Project(ModelWithRequiredID):
    company_id: str | None
    creator_id: str | None
    creator_type: str | None
    creator_name: str | None
    status: Literal["active", "deleted"] | None
    name: str | None
    address: Address | None
    coordinates: Coordinate | None
    featured_image: list[ImageURI] | None
    project_url: str | None
    embedded_project_url: str | None
    integrations: list[ProjectIntegration] | None
    slug: str | None
    public: bool | None
    geofence: list[Coordinate] | None
    primary_contact: ProjectContactResponse | None
    notepad: str | None
    created_at: int | None
    updated_at: int | None
