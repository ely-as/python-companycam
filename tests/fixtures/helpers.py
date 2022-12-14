import collections
import re
import typing


def transform_postman_url(url: str) -> str:  # pragma: no cover
    return re.sub(r":[^/]*", "{}", url).replace("{{baseUrl}}", "")


def transform_postman_headers(  # pragma: no cover
    header: typing.Mapping,
) -> typing.Dict:
    return {h["key"]: h["value"] for h in header}


def transform_postman_collection(  # pragma: no cover
    data: typing.Mapping,
) -> typing.Dict:
    # Flatten the data for easy iteration
    flattened_data = [
        (path["request"], response)
        for component in data["item"]
        for path in component["item"]
        for response in path["response"]
        if str(response["code"]).startswith("2")
    ]
    # Rewrite the data into return dict
    return_dict: typing.Dict = collections.defaultdict(dict)
    for request, response in flattened_data:
        url = transform_postman_url(request["url"]["raw"])
        method = request["method"].lower()
        return_dict[url][method] = {
            "status_code": int(response["code"]),
            "headers": transform_postman_headers(response["header"]),
            "content": response["body"],
        }
    return return_dict
