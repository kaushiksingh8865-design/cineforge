from pathlib import Path

from app.ai.models.source import SourceFile


class SourceExtractor:

    @staticmethod
    async def extract(source: SourceFile) -> str:

        if source.source_type == "screenplay":
            if not source.content:
                raise ValueError(
                    "Screenplay source does not contain content."
                )

            return source.content

        if source.source_type == "uploaded_file":
            if not source.file_path:
                raise ValueError(
                    "Uploaded source does not have a file path."
                )

            path = Path(source.file_path)

            if not path.exists():
                raise FileNotFoundError(
                    f"Source file not found: {source.file_path}"
                )

            if path.suffix.lower() == ".txt":
                return path.read_text(
                    encoding="utf-8"
                )

            raise ValueError(
                f"Unsupported file type: {path.suffix}"
            )

        raise ValueError(
            f"Unsupported source type: {source.source_type}"
        )