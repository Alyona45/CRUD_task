import asyncio
import ssl
from urllib.parse import urljoin

import aioboto3
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException, status

from app.settings import (
    MINIO_ACCESS_KEY,
    MINIO_BUCKET,
    MINIO_HEALTH_HOST,
    MINIO_HEALTH_PATH,
    MINIO_HEALTH_PORT,
    MINIO_HEALTH_SSL,
    MINIO_ENDPOINT,
    MINIO_PUBLIC_URL,
    MINIO_REGION,
    MINIO_SECRET_KEY,
)


async def check_storage_health() -> bool:
    ssl_context = ssl.create_default_context() if MINIO_HEALTH_SSL else None
    reader = None
    writer = None

    try:
        reader, writer = await asyncio.open_connection(
            host=MINIO_HEALTH_HOST,
            port=MINIO_HEALTH_PORT,
            ssl=ssl_context,
        )
        request = (
            f"GET {MINIO_HEALTH_PATH} HTTP/1.1\r\n"
            f"Host: {MINIO_HEALTH_HOST}\r\n"
            "Connection: close\r\n\r\n"
        )
        writer.write(request.encode("ascii"))
        await writer.drain()
        response = await reader.read(1024)
    except OSError:
        return False
    finally:
        if writer is not None:
            writer.close()
            await writer.wait_closed()

    return b"200 OK" in response


async def upload_file_to_storage(content: bytes, key: str, content_type: str) -> str:
    session = aioboto3.Session()

    try:
        async with session.client(
            "s3",
            endpoint_url=MINIO_ENDPOINT,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
            region_name=MINIO_REGION,
        ) as client:
            try:
                await client.head_bucket(Bucket=MINIO_BUCKET)
            except ClientError:
                create_bucket_kwargs = {"Bucket": MINIO_BUCKET}
                if MINIO_REGION != "us-east-1":
                    create_bucket_kwargs["CreateBucketConfiguration"] = {
                        "LocationConstraint": MINIO_REGION,
                    }
                await client.create_bucket(**create_bucket_kwargs)

            await client.put_object(
                Bucket=MINIO_BUCKET,
                Key=key,
                Body=content,
                ContentType=content_type,
            )
    except (ClientError, BotoCoreError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Storage is unavailable",
        ) from exc

    base_url = MINIO_PUBLIC_URL.rstrip("/") + "/"
    return urljoin(base_url, f"{MINIO_BUCKET}/{key}")
