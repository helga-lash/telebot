from helpers.work_classes import AppConf, PgConf, MinioClientConf, ReturnEntity
from helpers.configuration import logger, pg_conf, app_conf, minio_conf


postgresql_configuration: ReturnEntity = pg_conf()
application_configuration: ReturnEntity = app_conf()
minio_configuration: ReturnEntity = minio_conf()

if postgresql_configuration.error:
    logger.critical(postgresql_configuration.errorText)
    exit(1)

if application_configuration.error:
    logger.critical(application_configuration.errorText)
    exit(1)

pgs_conf: PgConf = postgresql_configuration.entity
apl_conf: AppConf = application_configuration.entity
mn_conf: MinioClientConf = minio_configuration.entity


__all__ = (
    'logger',
    'pgs_conf',
    'apl_conf',
    'mn_conf'
)
