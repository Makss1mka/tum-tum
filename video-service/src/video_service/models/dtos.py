from pydantic import BaseModel, Field
from .entities import VideoTag, Video

#
# VIDEO TAGS MODELS
#

class VideoTagCreateDto(BaseModel):
    """Data Transfer Object for creating a new video tag.
    
    Attributes:
        tag_name (str): The name of the tag to be created.
    """

    tag_name: str = Field(..., max_length=50, min_length=1)


class VideoTagResponseDto(BaseModel):
    """Data Transfer Object for video tag response.
    
    Attributes:
        id (int): The unique identifier of the tag.
        tag_name (str): The name of the tag.
    """

    id: int
    tag_name: str

    @staticmethod
    def from_entity(tag_entity: VideoTag) -> "VideoTagResponseDto":
        """Convert a VideoTag entity to a VideoTagResponseDto.
        
        Args:
            tag_entity (VideoTag): The VideoTag entity to convert.
            
        Returns:
            VideoTagResponseDto: The converted DTO.
        
        Raises:
            ValueError: If tag_entity is None.
            TypeError: If tag_entity is not an instance of VideoTag.
        """

        if not tag_entity:
            raise ValueError("Tag entity cannot be None")
        
        if not isinstance(tag_entity, VideoTag):
            raise TypeError("Expected tag_entity to be an instance of VideoTag")
        
        return VideoTagResponseDto(
            id=tag_entity.id,
            tag_name=tag_entity.tag_name
        )
    
    @staticmethod
    def from_entities_get_strs(tag_entities: list[VideoTag]) -> list[str]:
        """Convert a list of VideoTag entities to a list of tag names.
        
        Args:
            tag_entities (list[VideoTag]): The list of VideoTag entities to convert.
            
        Returns:
            list[str]: A list of tag names.
        
        Raises:
            ValueError: If tag_entities is None or empty.
            TypeError: If any item in tag_entities is not an instance of VideoTag.
        """

        if not tag_entities or not isinstance(tag_entities, list):
            raise ValueError("Tag entities cannot be None or empty")
        
        for tag_entity in tag_entities:
            if not isinstance(tag_entity, VideoTag):
                raise TypeError("Expected all items in tag_entities to be instances of VideoTag")
        
        return [tag.tag_name for tag in tag_entities]


#
# VIDEO'S MODELS
#

class VideoCreateDto(BaseModel):
    """Data Transfer Object for creating a new video.
    
    Attributes:
        title (str): The title of the video.
        description (str): A brief description of the video.
        tags (list[int]): List of tag IDs associated with the video.
        author_id (int): The ID of the author creating the video.
    """

    title: str = Field(None, max_length=150, min_length=1)
    description: str = Field(None, max_length=500, min_length=1)
    tags: list[int] = Field(default_factory=list)
    author_id: int = Field(..., max_length=36)


class VideoUpdateDto(BaseModel):
    """Data Transfer Object for updating an existing video.
    
    Attributes:
        video_id (int): The ID of the video to update.
        new_title (str): The new title for the video.
        new_description (str): The new description for the video.
        new_tags (list[int]): List of tag IDs to associate with the video.
    """

    new_title: str | None = Field(None, max_length=150)
    new_description: str | None = Field(None, max_length=500, min_length=1)
    new_tags: list[int] = Field(default_factory=list)


class VideoResponseDto(BaseModel):
    """Data Transfer Object for video response.
    
    Attributes:
        id (int): The unique identifier of the video.
        title (str): The title of the video.
        description (str): A brief description of the video.
        url (str): The URL where the video can be accessed.
        tags (list[str]): List of tags associated with the video.
    """

    id: int
    title: str
    description: str
    url: str
    tags: list[str]

    @staticmethod
    def from_entity(video_entity: Video) -> "VideoResponseDto":
        """Convert a Video entity to a VideoResponseDto.
        
        Args:
            video_entity (Video): The Video entity to convert.
            
        Returns:
            VideoResponse: The converted DTO.
        
        Raises:
            ValueError: If video_entity is None.
            TypeError: If video_entity is not an instance of Video.
        """

        if not video_entity:
            raise ValueError("Video entity cannot be None")
        
        if not isinstance(video_entity, Video):
            raise TypeError("Expected video_entity to be an instance of Video")
        
        return VideoResponseDto(
            id=video_entity.id,
            title=video_entity.title,
            description=video_entity.description,
            url=video_entity.file_video_path,
            tags= VideoTagResponseDto.from_entities_get_strs(video_entity.tags)
        )

