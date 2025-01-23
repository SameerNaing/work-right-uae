from pydantic import BaseModel
from typing import Optional, Dict, Any


class DocumentMetadata(BaseModel):
    source_url: str
    title: str
    is_file: bool

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert metadata to a dictionary. Automatically excludes fields with None values.
        """
        return self.model_dump(exclude_unset=True)

    @staticmethod
    def to_filter_dict(
        self,
        source_url: Optional[bool] = None,
        title: Optional[bool] = None,
        is_file: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Create a dictionary with selected fields for filtering based on the provided arguments.

        Args:
            source_url (Optional[bool]): Whether to include the `source_url` in the filter.
            title (Optional[bool]): Whether to include the `title` in the filter.
            is_file (Optional[bool]): Whether to include the `is_file` in the filter.

        Returns:
            Dict[str, Any]: A dictionary containing only the fields specified in the filter.
        """
        filter_dict = {}
        if source_url:
            filter_dict["source_url"] = self.source_url
        if title:
            filter_dict["title"] = self.title
        if is_file:
            filter_dict["is_file"] = self.is_file
        return filter_dict
