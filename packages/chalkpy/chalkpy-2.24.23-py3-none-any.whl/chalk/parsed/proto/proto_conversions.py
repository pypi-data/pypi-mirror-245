from typing import Any, Optional

from chalk.parsed.json_conversions import convert_type_to_gql


def convert_type_to_proto(t: Any, path_prefix: Optional[str] = None):
    return convert_type_to_gql(t, path_prefix).to_proto()
