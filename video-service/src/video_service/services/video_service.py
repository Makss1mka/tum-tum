"""Video Service Module"""

from exceptions import NotFoundException, BadRequestException, ConflictException, NoContentException, InternalServerErrorException
from models.dtos import VideoTagCreateDto, VideoTagResponseDto, \
    VideoCreateDto, VideoUpdateDto, VideoResponseDto
from models.entities import VideoTag, Video, UserData, VideoStatus
from utils.enums import VideoStatus as VideoStatusEnum
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import AsyncSessionMaker
from log.loggers import VIDEO_SERVICE_LOGGER
from log.wrappers import log_entrance_debug
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import joinedload


@log_entrance_debug(VIDEO_SERVICE_LOGGER)
async def create_video(video_dto: VideoCreateDto) -> VideoResponseDto:
    """Create a new video in the database.

    Args:
        video_dto (VideoCreateDto): The DTO containing video creation data.

    Returns:
        VideoResponseDto: The DTO of the created video.

    Raises:
        BadRequestException: If the video creation fails.
    """

    async with AsyncSessionMaker() as session:
        session: AsyncSession

        async with session.begin():
            try:
                new_video = Video(
                    title=video_dto.title,
                    description=video_dto.description,
                    author_id=video_dto.author_id,
                    status_id=VideoStatus.WAIT_FOR_VIDEO_FILE.get_num_value()
                )
            
                existing_tags: list[VideoTag] = session.select(VideoTag).all()
                existing_tags_str: list[str] = [tag.tag_name for tag in existing_tags]
                not_found_tags: list[VideoTag] = []

                for tag in video_dto.tags:
                    tag_ind = -1
                    for i in range(len(existing_tags_str)):
                        if existing_tags_str[i] == tag:
                            tag_ind = i
                            break

                    if tag_ind == -1:
                        not_found_tags.append(VideoTag(tag_name=tag))
                    else:
                        new_video.tags.append(existing_tags[tag_ind])\
                        
                if len(not_found_tags) > 0:
                    VIDEO_SERVICE_LOGGER.info(f"Creating new tags: {not_found_tags}")
                    session.add_all(not_found_tags)
                    session.refresh(not_found_tags)
                    new_video.tags.extend(not_found_tags)

                session.add(new_video)

                return VideoResponseDto.from_entity(new_video)
            
            except IntegrityError as e:
                VIDEO_SERVICE_LOGGER.exception(f"Integrity error creating video: {e}")
                raise ConflictException("Video ruins some uniques rules") from e
            
            except (ValueError, TypeError) as e:
                VIDEO_SERVICE_LOGGER.exception(f"Value or Type error creating video: {e}")
                raise BadRequestException("Invalid data provided for video creation") from e
            
            except Exception as e:
                VIDEO_SERVICE_LOGGER.exception(f"Error creating video: {e}")
                raise BadRequestException("Failed to create video") from e


@log_entrance_debug(VIDEO_SERVICE_LOGGER)
async def get_video_by_id(video_id: str) -> VideoResponseDto:
    """Retrieve a video by its ID.

    Args:
        video_id (str): The ID of the video to retrieve.

    Returns:
        VideoResponseDto: The DTO of the retrieved video.

    Raises:
        NotFoundException: If the video with the given ID does not exist.
    """

    async with AsyncSessionMaker() as session:
        async with session.begin():
            try:
                video: Video = (await session.execute(
                    select(Video)
                    .options(
                        joinedload(Video.author),
                        joinedload(Video.status),
                        joinedload(Video.tags)
                    )
                    .where(Video.id == video_id)
                )).scalars().first()

                if not video:
                    raise NotFoundException(f"Video with ID {video_id} not found")
                
                return VideoResponseDto.from_entity(video)
            
            except NotFoundException as e:
                VIDEO_SERVICE_LOGGER.warning(f"Video with ID {video_id} not found: {e}")
                raise NotFoundException(f"Video with ID {video_id} not found") from e

            except Exception as e:
                VIDEO_SERVICE_LOGGER.exception(f"Error retrieving video {video_id}: {e}")
                raise InternalServerErrorException("Unexpected exception") from e


@log_entrance_debug(VIDEO_SERVICE_LOGGER)
async def update_video(video_id: str, video_dto: VideoUpdateDto) -> VideoResponseDto:
    """Update an existing video.

    Args:
        video_id (str): The ID of the video to update.
        video_dto (VideoUpdateDto): The DTO containing updated video data.

    Returns:
        VideoResponseDto: The DTO of the updated video.

    Raises:
        NotFoundException: If the video with the given ID does not exist.
        BadRequestException: If the update fails due to invalid data.
    """

    async with AsyncSessionMaker() as session:
        session: AsyncSession

        async with session.begin():
            try:
                video: Video = (await session.execute(
                    select(Video)
                    .options(
                        joinedload(Video.author),
                        joinedload(Video.status),
                        joinedload(Video.tags)
                    )
                    .where(Video.id == video_id)
                )).scalars().first()

                if not video:
                    raise NotFoundException(f"Video with ID {video_id} not found")
                
                is_smth_changed: bool = False

                if video_dto.title is not None and video.title != video_dto.title:
                    is_smth_changed = True

                    video.title = video_dto.title
                if video_dto.description is not None and video.description != video_dto.description:
                    is_smth_changed = True

                    video.description = video_dto.description
                if video_dto.new_tags is not None and video_dto.new_tags != [tag.tag_name for tag in video.tags]:
                    is_smth_changed = True

                    video.tags.clear()
                    
                    existing_tags: list[VideoTag] = (await session.execute(
                        select(VideoTag)
                    )).scalars().all()

                    existing_tags_str: list[str] = [tag.tag_name for tag in existing_tags]
                    not_found_tags: list[VideoTag] = []

                    for tag in video_dto.new_tags:
                        tag_ind = -1
                        for i in range(len(existing_tags_str)):
                            if existing_tags_str[i] == tag:
                                tag_ind = i
                                break

                        if tag_ind == -1:
                            not_found_tags.append(VideoTag(tag_name=tag))
                        else:
                            video.tags.append(existing_tags[tag_ind])
                    
                    if len(not_found_tags) > 0:
                        VIDEO_SERVICE_LOGGER.info(f"Creating new tags: {not_found_tags}")
                        session.add_all(not_found_tags)
                        session.refresh(not_found_tags)

                    video.tags.extend(not_found_tags)
                
                if is_smth_changed:
                    return VideoResponseDto.from_entity(video)
                else:
                    raise NoContentException("No changes were made to the video")
            
            except IntegrityError as e:
                VIDEO_SERVICE_LOGGER.exception(f"Integrity error updating video {video_id}: {e}")
                raise ConflictException("Video update violates unique constraints") from e
            
            except NoContentException as e:
                VIDEO_SERVICE_LOGGER.warning(f"{e.message}: {e}")
                raise NoContentException(e.message) from e

            except NotFoundException as e:
                VIDEO_SERVICE_LOGGER.warning(f"{e.message}: {e}")
                raise NotFoundException(e.message) from e

            except (ValueError, TypeError) as e:
                VIDEO_SERVICE_LOGGER.exception(f"Value or Type error updating video {video_id}: {e}")
                raise BadRequestException("Invalid data provided for video update") from e

            except Exception as e:
                VIDEO_SERVICE_LOGGER.exception(f"Unexpected error updating video {video_id}: {e}")
                raise InternalServerErrorException("Failed to update video") from e
            

@log_entrance_debug(VIDEO_SERVICE_LOGGER)
async def delete_video(video_id: str) -> None:
    """Delete a video by its ID.

    Args:
        video_id (str): The ID of the video to delete.

    Raises:
        NotFoundException: If the video with the given ID does not exist.
        BadRequestException: If the deletion fails.
    """

    async with AsyncSessionMaker() as session:
        session: AsyncSession

        async with session.begin():
            try:
                video: Video = (await session.execute(
                    select(Video)
                    .where(Video.id == video_id)
                )).scalars().first()

                if not video:
                    raise NotFoundException(f"Video with ID {video_id} not found")
                
                await session.delete(video)
                await session.commit()
            
            except NotFoundException as e:
                VIDEO_SERVICE_LOGGER.warning(f"{e.message}: {e}")
                raise NotFoundException(e.message) from e

            except (ValueError, TypeError) as e:
                VIDEO_SERVICE_LOGGER.exception(f"Value or Type error deleting video {video_id}: {e}")
                raise BadRequestException("Invalid data provided for video deletion") from e

            except Exception as e:
                VIDEO_SERVICE_LOGGER.exception(f"Unexpected error deleting video {video_id}: {e}")
                raise InternalServerErrorException("Failed to delete video") from e




