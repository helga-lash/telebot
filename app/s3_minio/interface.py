from miniopy_async import Minio
from io import BytesIO
from datetime import timedelta

from configuration import logger, mn_conf, apl_conf
from helpers.work_classes import MinioClientConf, ReturnEntity


class MinioClient:
    def __init__(self, config: MinioClientConf = mn_conf) -> None:
        """
        Initialize a new instance of MinioClient.

        Parameters:
            config (MinioClientConf): The configuration for the Minio client. If not provided,
                                      the default configuration from `mn_conf` will be used.

        Returns:
            None
        """
        self.config = config
        self.client = Minio(
            endpoint=config.host + ':' + str(config.port),
            access_key=config.accessKey,
            secret_key=config.secretKey,
            secure=config.secure,
            region=config.region
        )

    async def __check_bucket(self, bucket: str) -> ReturnEntity:
        """
        Asynchronous method to check if a bucket exists in Minio.

        Parameters:
            bucket (str): The name of the bucket to check.

        Returns:
            ReturnEntity: An object containing the result of the operation.
                - entity (bool): True if the bucket exists, False otherwise.
                - error (bool): True if an error occurred during the operation, False otherwise.
                - error_text (str): Error message if an error occurred during the operation.
        """
        result: ReturnEntity = ReturnEntity(False)
        try:
            result.entity = await self.client.bucket_exists(bucket)
            logger.debug(f'Bucket {bucket} exists: {result.entity}')
        except Exception as error:
            result.error = True
            result.error_text_append(str(error))
            logger.debug(error)
        return result

    async def __create_bucket(self, bucket: str) -> ReturnEntity:
        """
        Asynchronous method to create a bucket in Minio.

        Parameters:
            bucket (str): The name of the bucket to create.

        Returns:
            ReturnEntity: An object containing the result of the operation.
                - entity (bool): True if the bucket was created, False otherwise.
                - error (bool): True if an error occurred during the operation, False otherwise.
                - error_text (str): Error message if an error occurred during the operation.
        """
        result: ReturnEntity = ReturnEntity(False)
        try:
            await self.client.make_bucket(bucket, location=self.config.region)
            result.entity = True
            logger.debug(f'Bucket {bucket} created.')
        except Exception as error:
            result.error = True
            result.error_text_append(str(error))
            logger.debug(error)
        return result

    async def upload(self, bucket: str, filename: str, data: BytesIO, size: int) -> ReturnEntity:
        """
        Asynchronously uploads a file to a specified bucket in Minio.

        If the bucket does not exist, it will be created.

        Parameters:
            bucket (str): The name of the bucket to upload the file to.
            filename (str): The name of the file to be uploaded.
            data (BytesIO): The file data to be uploaded.
            size (int): The size of the file data in bytes.

        Returns:
            ReturnEntity: An object containing the result of the operation.
                entity (bool): True if the file was uploaded successfully, False otherwise.
                error (bool): True if an error occurred during the operation, False otherwise.
                error_text (str): Error message if an error occurred during the operation.
        """
        result: ReturnEntity = ReturnEntity(False)
        check_bucket = await self.__check_bucket(bucket)
        if check_bucket.error:
            result.error = True
            result.error_text_append(check_bucket.errorText)
            return result
        if not check_bucket.entity:
            create_bucket = await self.__create_bucket(bucket)
            if create_bucket.error:
                result.error = True
                result.error_text_append(create_bucket.errorText)
                return result
        try:
            await self.client.put_object(bucket, filename, data, size)
            result.entity = True
            logger.debug(f'File {filename} uploaded to bucket {bucket}.')
        except Exception as error:
            result.error = True
            result.error_text_append(str(error))
            logger.debug(error)
        return result

    async def return_photo_names(self, bucket: str) -> ReturnEntity:
        """
        Asynchronously returns a list of file names in a specified bucket in Minio.

        Parameters:
            bucket (str): The name of the bucket to return the file names from.
        """
        result: ReturnEntity = ReturnEntity(False)
        check_bucket = await self.__check_bucket(bucket)
        if check_bucket.error:
            result.error = True
            result.error_text_append(check_bucket.errorText)
            return result
        try:
            objects = await self.client.list_objects(bucket)
            if objects is None:
                result.error = True
                result.error_text_append(f'Bucket {bucket} is empty')
                return result
            result.entity = [obj.object_name for obj in objects]
        except Exception as error:
            result.error = True
            result.error_text_append(str(error))
            logger.debug(error)
        return result

    async def download(self, bucket: str, filename: str) -> ReturnEntity:
        result: ReturnEntity = ReturnEntity(False)
        check_bucket = await self.__check_bucket(bucket)
        if check_bucket.error:
            result.error = True
            result.error_text_append(check_bucket.errorText)
            return result
        try:
            file_path = f'{str(apl_conf.tgBot.photoPath)}/{filename}'
            await self.client.fget_object(bucket, filename, file_path)
            result.entity = file_path
        except Exception as error:
            result.error = True
            result.error_text_append(str(error))
            logger.debug(error)
        return result
