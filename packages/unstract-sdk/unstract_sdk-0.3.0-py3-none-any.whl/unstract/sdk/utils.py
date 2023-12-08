from hashlib import md5


class ToolUtils:
    """Class containing utility methods."""

    @staticmethod
    def hash_str(string_to_hash: str, hash_method: str = "md5") -> str:
        """Computes the hash for a given input string.

        Useful to hash strings needed for caching and other purposes.
        Hash method defaults to "md5"

        Args:
            string_to_hash (str): String to be hashed
            hash_method (str): Hash hash_method to use, supported ones
                - "md5"

        Returns:
            str: Hashed string
        """
        if hash_method == "md5":
            if isinstance(string_to_hash, bytes):
                return str(md5(string_to_hash).hexdigest())
            return str(md5(string_to_hash.encode()).hexdigest())
        else:
            raise ValueError(f"Unsupported hash_method: {hash_method}")
