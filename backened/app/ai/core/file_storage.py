from pathlib import Path
from uuid import uuid4


class FileStorage:

    def __init__(self, base_path: str = "storage"):
        self.base_path = Path(base_path)

    async def save(
        self,
        file_content: bytes,
        original_filename: str,
    ) -> str:

        self.base_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        extension = Path(original_filename).suffix

        stored_filename = f"{uuid4()}{extension}"

        file_path = self.base_path / stored_filename

        file_path.write_bytes(file_content)

        return str(file_path)

    async def delete(
        self,
        file_path: str,
    ) -> bool:

        path = Path(file_path)

        if not path.exists():
            return False

        path.unlink()

        return True