from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, HTTPException
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from src.files.s3_bucket_config import s3_client
from sqlalchemy import select, insert
from src.files.schemas import MediaOut
from config import S3_BUCKET_NAME
from src.auth.models import User
from src.files.models import File
import tempfile
import os


###comment to push233
async def upload_an_image(file, session, user):

    # is_user(user.role_id)
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=418, detail="Only .png and .jpeg images are allowed")
    else:
        file_extension = "jpeg" if file.content_type == "image/jpeg" else "png"
        file_name = f'media/{user.id}_{uuid4()}.{file_extension}'

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            file_content = await file.read()
            temp_file.write(file_content)

        # Create a temporary file to save the uploaded content

        s3_client.upload_file(temp_path, S3_BUCKET_NAME, file_name)

        url = s3_client.generate_presigned_url('get_object', Params={'Bucket': S3_BUCKET_NAME,
                                                                     'Key': file_name},
                                               ExpiresIn=3600)

        os.remove(temp_path)

        details = {
            "file_name": file_name,
            "user_id": user.id
        }

        stmt = insert(File).values(**details)
        await session.execute(stmt)
        await session.commit()

        query = select(File).order_by(File.created_at.desc())
        last_created_file = await session.execute(query)
        result = last_created_file.scalars().first()

        return MediaOut(id=result.id, file=url)


async def get_avatar(user_id, session):
    query = select(File).join(User, onclause=File.id == User.avatar_id).where(User.id == user_id)
    post_media = await session.execute(query)
    response = post_media.scalar_one_or_none()

    if response is None:
        return None
    else:
        url = s3_client.generate_presigned_url('get_object', Params={'Bucket': S3_BUCKET_NAME,
                                                                     'Key': response.file_name},
                                               ExpiresIn=3600)
        return MediaOut(id=response.id, file=url)




