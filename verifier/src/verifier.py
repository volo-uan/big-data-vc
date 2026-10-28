from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
from botocore.exceptions import ClientError

app = FastAPI()

BUCKET = "zweryfikowane"


class UploadRequest(BaseModel):
    filename: str
    content: str


def get_s3():
    return boto3.client(
        "s3",
        endpoint_url="http://minio:9000",
        aws_access_key_id="student",
        aws_secret_access_key="student123",
    )


@app.post("/upload")
def upload_file(data: UploadRequest):

    if not data.filename.endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="only .txt files allowed"
        )

    s3 = get_s3()

    try:
        s3.head_bucket(Bucket=BUCKET)
    except ClientError:
        s3.create_bucket(Bucket=BUCKET)

    s3.put_object(
        Bucket=BUCKET,
        Key=data.filename,
        Body=data.content.encode()
    )

    return {
        "saved": f"{BUCKET}/{data.filename}",
        "size": len(data.content)
    }


@app.get("/files")
def files():

    s3 = get_s3()

    try:
        result = s3.list_objects_v2(Bucket=BUCKET)
    except ClientError:
        return []

    return [
        obj["Key"]
        for obj in result.get("Contents", [])
    ]