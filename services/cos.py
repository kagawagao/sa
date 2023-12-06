from qcloud_cos import CosConfig, CosS3Client

from configs.cos import COS_BUCKET, COS_REGION, COS_SECRET_ID, COS_SECRET_KEY

cos_config = CosConfig(Region=COS_REGION, SecretId=COS_SECRET_ID,
                       SecretKey=COS_SECRET_KEY, Token=None, Scheme="https")

cos_client = CosS3Client(conf=cos_config)


def download_cos_file(key: str, dest: str):
    """下载 COS 文件"""
    cos_client.download_file(
        Bucket=COS_BUCKET,
        Key=key,
        DestFilePath=dest
    )


def get_presigned_url(key: str) -> str:
    """获取 COS 文件的预签名 URL"""
    return cos_client.get_presigned_url(
        Bucket=COS_BUCKET,
        Key=key,
        Method="PUT"
    )


def list_cos_objects(prefix: str = ""):
    """获取 COS 对象数量"""
    contents = []
    marker = ""
    while True:
        response = cos_client.list_objects(
            Bucket=COS_BUCKET,
            Prefix=prefix,
            Marker=marker,
            MaxKeys=1000,
        )
        if "Contents" in response:
            contents.extend(response["Contents"])
        if "Contents" not in response or response['IsTruncated'] == 'false':
            break
        marker = response["NextMarker"]

    return {
        "total": len(contents),
        "items": contents
    }


def check_object_exist(key: str):
    """检查 COS 对象是否存在"""
    return cos_client.object_exists(
        Bucket=COS_BUCKET,
        Key=key
    )


def upload_object(key: str, local_path: str):
    """上传 COS 对象"""
    res = cos_client.upload_file(
        Bucket=COS_BUCKET,
        Key=key,
        LocalFilePath=local_path
    )
    return res


if __name__ == "__main__":
    print(get_presigned_url("test.txt"))
    print(list_cos_objects("test/"))
    print(check_object_exist("test.txt"))
