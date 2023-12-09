"""Course Progress static vars."""

BASE_URL = "https://{INSTANCE_NAME}.coursepro.co.uk/rest"
ENDPOINT_MAP = {
    "login": {"endpoint": "/authenticate", "method": "POST"},
    "refresh": {"endpoint": "/authenticate"},
    "get_members": {"endpoint": "/members"},
    "get_member": {"endpoint": "/members/{MEMBER_ID}"},
    "get_classes_history": {"endpoint": "/members/{MEMBER_ID}/classeshistory"},
    "get_badges": {"endpoint": "/members/{MEMBER_ID}/badges"},
    "get_class": {"endpoint": "/members/{MEMBER_ID}/classes/{CLASS_ID}"},
    "get_competencies": {"endpoint": "/members/{MEMBER_ID}/classes/{CLASS_ID}/competencies"},
    "get_sessions": {"endpoint": "/members/{MEMBER_ID}/classes/{CLASS_ID}/sessions"},
}
