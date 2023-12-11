import datetime


def cache_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return {
            "__type__": "datetime",
            "isoformat": obj.isoformat()
        }
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def decrypt_datetime(obj):
    if "__type__" in obj and obj["__type__"] == "datetime":
        return datetime.datetime.fromisoformat(obj["isoformat"])
    return obj
