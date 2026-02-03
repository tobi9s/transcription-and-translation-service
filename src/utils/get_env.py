import os
    
def get_env(var: str):
    """
    Get an environment variable.
    """
    value = os.getenv(var)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {var}")
    return value