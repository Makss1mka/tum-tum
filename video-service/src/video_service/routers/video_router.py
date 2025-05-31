from fastapi import APIRouter, Response
from services import video_service
from models.dtos import VideoCreateDto, VideoUpdateDto, VideoResponseDto

video_router = APIRouter()


@video_router.post("/")
async def create_video(resp: Response, video_dto: VideoCreateDto) -> VideoResponseDto:
    """Creates a new video.

    Args:
        resp (Response): Response object.
        video_dto (VideoCreateDto): Video data transfer object.

    Returns:
        VideoResponseDto: Video response data transfer object.
    """
    video_response = await video_service.create_video(video_dto)
    resp.status_code = 201
    
    return video_response


@video_router.put("/{video_id}")
async def update_video(video_id: str, video_dto: VideoUpdateDto) -> VideoResponseDto:
    """Updates an existing video.

    Args:
        video_id (str): ID of the video to update.
        video_dto (VideoUpdateDto): Video data transfer object with updated information.

    Returns:
        VideoResponseDto: Updated video response data transfer object.
    """
    return await video_service.update_video(video_id, video_dto)


@video_router.delete("/{video_id}")
async def delete_video(video_id: str) -> dict:
    """Deletes a video.

    Args:
        video_id (str): ID of the video to delete.

    Returns:
        None
    """
    await video_service.delete_video(video_id)
    return {"message": "Video deleted successfully"}


@video_router.get("/{video_id}")
async def get_video_by_id(video_id: str) -> VideoResponseDto:
    """Retrieves a video by its ID.

    Args:
        video_id (str): ID of the video to retrieve.

    Returns:
        VideoResponseDto: Video response data transfer object.
    """
    return await video_service.get_video(video_id)
