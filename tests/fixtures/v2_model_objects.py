import io

from companycam.v2 import models


class TestFile(io.BytesIO):
    """So when passed to BufferedReader it has a `name` attribute to access"""

    name: str = "test.txt"


TAG = models.Tag(
    id="48892885",
    company_id="8292212",
    display_value="Front Side",
    value="front side",
    created_at=1152230608,
    updated_at=1152230700,
)


# Keys have same names as the keyword arguments in manager paths for easy lookup
KWARGS = {
    "captured_at": 1152230608,
    "comment": models.Comment(
        id="4782987471",
        creator_id="2789583992",
        creator_type="User",
        creator_name="Shawn Spencer",
        commentable_id="388472672",
        commentable_type="Photo",
        status="active",
        content="Have you seen this yet?",
        created_at=1152230608,
        updated_at=1152230400,
    ),
    "coordinates": models.Coordinate(lat=-82437315.85179588, lon=80048850.74793434),
    "document": models.Document(
        id="115",
        creator_id="8675309",
        creator_type="User",
        creator_name="CompanyCam Developer",
        project_id="48892885",
        name="silver-kadabra-measurements.pdf",
        url="https://static.companycam.com/documents/8374c65e-2048-41d4-b4a7-a9c839fd388a.pdf",
        content_type="application/pdf",
        byte_size=3457903,
        created_at=1621857746,
        updated_at=1621857746,
    ),
    "file": io.BufferedReader(TestFile(b"test document")),  # type: ignore[arg-type]
    "group": models.Group(
        id="3992883",
        company_id="8292212",
        name="The Psych Crew",
        users=[
            {
                "id": "2789583992",
                "company_id": "8292212",
                "email_address": "shawn@psych.co",
                "status": "active",
                "first_name": "Shawn",
                "last_name": "Spencer",
                "profile_image": [
                    {"type": "aliquip in officia", "uri": "qui sit"},
                    {"type": "minim dolore laboris ir", "uri": "in"},
                ],
                "phone_number": "4025551212",
                "created_at": 1490737206,
                "updated_at": 1490737206,
                "user_url": "https://app.companycam.com/users/1234",
            },
            {
                "id": "2789583992",
                "company_id": "8292212",
                "email_address": "shawn@psych.co",
                "status": "active",
                "first_name": "Shawn",
                "last_name": "Spencer",
                "profile_image": [
                    {"type": "irure fu", "uri": "non"},
                    {
                        "type": "sit ipsum incididunt anim consequat",
                        "uri": "reprehenderit",
                    },
                ],
                "phone_number": "4025551212",
                "created_at": 1490737206,
                "updated_at": 1490737206,
                "user_url": "https://app.companycam.com/users/1234",
            },
        ],
        status="active",
        group_url="https://app.companycam.com/groups/1234",
        created_at=1490737206,
        updated_at=1490737744,
    ),
    "invitation": models.ProjectInvitation(
        id="4782987471",
        project_id="94772883",
        invite_url="https://l.cmpy.cam/9vT849PkgrVqpYb8A",
        status="pending",
        accepted_at=None,
        accepted_by_id=None,
        expires_at=1671580800,
        permissions=[
            "can_view_content",
            "can_add_content",
            "can_comment",
            "can_use_todos",
        ],
        creator_id="2789583992",
        created_at=1152230608,
        updated_at=1152230400,
    ),
    "label": TAG.copy(deep=True),
    "photo": models.Photo(
        id="4782987471",
        company_id="8292212",
        creator_id="2789583992",
        creator_type="User",
        creator_name="Shawn Spencer",
        project_id="94772883",
        processing_status="processed",
        coordinates=[
            {"lat": -82437315.85179588, "lon": 80048850.74793434},
            {"lat": 10068001.054838628, "lon": -49589187.34253812},
        ],
        urls=[{"type": "et", "uri": "cul"}, {"type": "culpa", "uri": "eu minim"}],
        hash="00ab337b7399151e5d4aa3bd4226e8dd",
        internal=False,
        photo_url="https://app.companycam.com/photos/8675309",
        captured_at=1152230396,
        created_at=1152230608,
        updated_at=1152230400,
    ),
    "project": models.Project(
        id="94772883",
        company_id="8292212",
        creator_id="2789583992",
        creator_type="User",
        creator_name="Shawn Spencer",
        status="active",
        name="Psych Office",
        address={
            "street_address_1": "808 P St",
            "city": "Lincoln",
            "state": "NE",
            "postal_code": "68508",
            "country": "US",
        },
        coordinates={"lat": 7846226.309591979, "lon": -52765352.88495099},
        featured_image=[
            {"type": "deserunt in", "uri": "Ut elit"},
            {"type": "magna Ut quis", "uri": "nisi incididunt dolor"},
        ],
        project_url="https://app.companycam.com/projects/1234",
        embedded_project_url="https://app.companycam.com/embed/projects/QrL2XjgF8P2dN6MPDRdV2Q",
        integrations=[
            {"type": "JobNimbus", "relation_id": "123"},
            {"type": "JobNimbus", "relation_id": "123"},
        ],
        slug="QrL2XjgF8P2dN6MPDRdV2Q",
        public=False,
        geofence=[
            {"lat": -53958026.2273736, "lon": 87619210.1236322},
            {"lat": -18473456.467655286, "lon": -97157675.7681222},
        ],
        primary_contact=None,
        notepad="Notes",
        created_at=1152230400,
        updated_at=1395792000,
    ),
    "tag": TAG.copy(deep=True),
    "uri": "https://static.companycam.com/lambda/projects/94772883/photos/bHR0.jpg",
    "user": models.User(
        id="2789583992",
        company_id="8292212",
        email_address="shawn@psych.co",
        status="active",
        first_name="Shawn",
        last_name="Spencer",
        profile_image=[
            {"type": "adipisicing non", "uri": "cillum sit do"},
            {"type": "fugiat laborum mollit", "uri": "quis et"},
        ],
        phone_number="4025551212",
        created_at=1490737206,
        updated_at=1490737206,
        user_url="https://app.companycam.com/users/1234",
    ),
    "webhook": models.Webhook(
        id="labore Ut laborum consequat",
        company_id="tempor elit",
        url="Ut consequat",
        scopes=["commodo", "cupidatat sun"],
        token="aliquip",
        enabled=False,
        created_at=41172137,
        updated_at=81586808,
    ),
}
