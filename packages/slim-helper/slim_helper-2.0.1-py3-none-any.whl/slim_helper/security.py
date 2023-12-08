import hashlib
from pathlib import Path


def sha3_512(obj: Path | str | bytes) -> str:
    """SHA3-512

    Args:
        obj (Path | str | bytes): file path or string

    Raises:
        RuntimeError: Unsupported argument type

    Returns:
        str: hex digest
    """
    if isinstance(obj, Path):
        hash_sha512 = hashlib.sha3_512()
        with open(obj, "rb") as f:
            for chunk in iter(lambda: f.read(1048576), b""):
                hash_sha512.update(chunk)
        return hash_sha512.hexdigest()
    elif isinstance(obj, str):
        obj: str
        digest = hashlib.sha3_512(obj.encode("utf8"))
        return digest.hexdigest()
    elif isinstance(obj, bytes):
        obj: bytes
        digest = hashlib.sha3_512(obj)
        return digest.hexdigest()
    else:
        raise RuntimeError("Unsupported argument type")
