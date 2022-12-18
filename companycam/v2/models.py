from typing import List, Literal, Optional

from companycam.models import Model, ModelWithRequiredID

# Components which don't reference other components, alphabetical


class Address(Model):
    street_address_1: Optional[str]
    street_address_2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]


class Comment(ModelWithRequiredID):
    creator_id: Optional[str]
    creator_type: Optional[str]
    creator_name: Optional[str]
    commentable_id: Optional[str]
    commentable_type: Optional[str]
    status: Optional[str]
    content: Optional[str]
    created_at: Optional[int]
    updated_at: Optional[int]


class Coordinate(Model):
    lat: float
    lon: float


class Document(ModelWithRequiredID):
    creator_id: Optional[str]
    creator_type: Optional[str]
    creator_name: Optional[str]
    project_id: Optional[str]
    name: Optional[str]
    url: Optional[str]
    content_type: Optional[str]
    byte_size: Optional[int]
    created_at: Optional[int]
    updated_at: Optional[int]


class Error(Model):
    errors: Optional[List[str]]


class ImageURI(Model):
    type: str
    uri: str

    class Config:
        assignment_aliases = {"url": "uri"}


class ProjectCollaborator(Model):
    id: Optional[str]
    company_id: Optional[str]
    project_id: Optional[str]
    project_invitation_id: Optional[str]
    permissions: Optional[
        List[
            Literal[
                "can_view_content", "can_add_content", "can_comment", "can_use_todos"
            ]
        ]
    ]
    accepted_at: Optional[int]
    created_at: Optional[int]
    updated_at: Optional[int]


class ProjectContactRequest(Model):
    name: str
    email: Optional[str]
    phone_number: Optional[str]


class ProjectContactResponse(Model):
    id: Optional[str]
    project_id: Optional[str]
    name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    created_at: Optional[int]
    updated_at: Optional[int]


class ProjectInvitation(Model):
    id: Optional[str]
    project_id: Optional[str]
    invite_url: Optional[str]
    status: Optional[Literal["accepted", "expired", "pending"]]
    accepted_at: Optional[int]
    accepted_by_id: Optional[str]
    expires_at: Optional[int]
    permissions: Optional[
        List[
            Literal[
                "can_view_content", "can_add_content", "can_comment", "can_use_todos"
            ]
        ]
    ]
    creator_id: Optional[str]
    created_at: Optional[int]
    updated_at: Optional[int]


class ProjectIntegration(Model):
    type: str
    relation_id: str


class ProjectNotepad(Model):
    notepad: str


class Tag(ModelWithRequiredID):
    company_id: Optional[str]
    display_value: Optional[str]
    value: Optional[str]
    created_at: Optional[int]
    updated_at: Optional[int]


class Webhook(ModelWithRequiredID):
    company_id: Optional[str]
    url: Optional[str]
    scopes: Optional[List[str]]
    token: Optional[str]
    enabled: Optional[bool]
    created_at: Optional[int]
    updated_at: Optional[int]


# Components which reference other components, alphabetical


class User(ModelWithRequiredID):
    company_id: Optional[str]
    email_address: Optional[str]
    status: Optional[Literal["active", "deleted"]]
    first_name: Optional[str]
    last_name: Optional[str]
    profile_image: Optional[List[ImageURI]]
    phone_number: Optional[str]
    created_at: Optional[int]
    updated_at: Optional[int]
    user_url: Optional[str]


# Rest of the components which reference other components, alphabetical


class Company(ModelWithRequiredID):
    name: str
    status: Optional[Literal["active", "cancelled", "deleted"]]
    address: Optional[Address]
    logo: Optional[List[ImageURI]]


class Group(ModelWithRequiredID):
    company_id: Optional[str]
    name: Optional[str]
    users: Optional[List[User]]
    status: Optional[Literal["active", "deleted"]]
    group_url: Optional[str]
    created_at: Optional[int]
    updated_at: Optional[int]


class Photo(ModelWithRequiredID):
    company_id: Optional[str]
    creator_id: Optional[str]
    creator_type: Optional[str]
    creator_name: Optional[str]
    project_id: Optional[str]
    processing_status: Optional[
        Literal["pending", "processing", "processed", "processing_error", "duplicate"]
    ]
    coordinates: Optional[List[Coordinate]]
    urls: Optional[List[ImageURI]]
    hash: Optional[str]
    internal: Optional[bool]
    photo_url: Optional[str]
    captured_at: Optional[int]
    created_at: Optional[int]
    updated_at: Optional[int]

    class Config:
        assignment_aliases = {"uris": "urls"}

    def __init__(self, *args, **kwargs) -> None:
        # Coerce `coordinates` to a list if dict is received in HTTP response
        if coordinates := kwargs.get("coordinates"):
            if isinstance(coordinates, dict):
                kwargs["coordinates"] = [coordinates]
        super().__init__(*args, **kwargs)


class Project(ModelWithRequiredID):
    company_id: Optional[str]
    creator_id: Optional[str]
    creator_type: Optional[str]
    creator_name: Optional[str]
    status: Optional[Literal["active", "deleted"]]
    name: Optional[str]
    address: Optional[Address]
    coordinates: Optional[Coordinate]
    featured_image: Optional[List[ImageURI]]
    project_url: Optional[str]
    embedded_project_url: Optional[str]
    integrations: Optional[List[ProjectIntegration]]
    slug: Optional[str]
    public: Optional[bool]
    geofence: Optional[List[Coordinate]]
    primary_contact: Optional[ProjectContactResponse]
    notepad: Optional[str]
    created_at: Optional[int]
    updated_at: Optional[int]
