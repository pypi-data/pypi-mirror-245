from pydantic import ConfigDict

PYDANTIC_CONFIG: ConfigDict = {
    "allow_inf_nan": False,
    "arbitrary_types_allowed": True,
    "strict": True,
    "validate_default": True,
}
