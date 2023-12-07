
from tencentcloud.common.profile import http_profile, client_profile
from tencentcloud.common.credential import Credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.dlc.v20210125 import dlc_client, models, errorcodes
from tdlc_connector import constants, exceptions

from qcloud_cos import CosS3Client, CosConfig

import base64
import json
import logging 
import urllib.parse



LOG = logging.getLogger("APIClient")


class APIClient:
    
    def __init__(self, region, secret_id, secret_key, token=None, dlc_endpoint=None, cos_endpoint=None):

        self._region = region
        self._cos_endpoint = cos_endpoint

        credential = Credential(secret_id, secret_key, token)
        profile = client_profile.ClientProfile(httpProfile=http_profile.HttpProfile(endpoint=dlc_endpoint))

        self._DLC_CLIENT = WrappedDlcClient(credential, region, profile)
        self.patch_cos_client(secret_id, secret_key, token)


    def patch_cos_client(self, secret_id, secret_key, token=None):

        config = CosConfig(Region=self._region, Secret_id=secret_id, Secret_key=secret_key, Token=token, Endpoint=self._cos_endpoint)
        self._COS_CLIENT = CosS3Client(config)
    

    def describe_engine_type(self, name):

        request = models.DescribeDataEnginesRequest()
        filter = models.Filter()
        filter.Name = 'data-engine-name'
        filter.Values = [name, ]
        request.Filters = [filter]


        response = self._DLC_CLIENT.DescribeDataEngines(request)

        if response.TotalCount == 0:
            raise exceptions.ProgrammingError(f"The engine[{name}] is not exists.")
        
        engine = response.DataEngines[0]

        if engine.EngineType == 'presto':
            return constants.EngineType.PRESTO
        
        if engine.EngineType == 'spark':
            if engine.EngineExecType == 'SQL':
                return constants.EngineType.SPARK_SQL
            elif engine.EngineExecType == 'BATCH':
                return constants.EngineType.SPARK_BATCH
        
        return constants.EngineType.UNKNOWN


    def submit_statement_to_spark_batch(self, engine, driver_size, executor_size, executor_num, executor_max_num, statement, config={}):

        request = models.CreateSparkSessionBatchSQLRequest()
        request.DataEngineName = engine
        request.DriverSize = driver_size
        request.ExecutorSize = executor_size
        request.ExecutorNumbers = executor_num
        request.ExecutorMaxNumbers = executor_max_num
        request.ExecuteSQL = base64.b64encode(statement.encode('utf8')).decode('utf8')
        request.Arguments = []

        if 'dlc.eni' in config:
            pair = models.KVPair()
            pair.Key = 'dlc.eni'
            pair.Value = config.pop('dlc.eni')
            request.Arguments.append(pair)
        
        if 'dlc.role.arn' in config:
            pair = models.KVPair()
            pair.Key = 'dlc.role.arn'
            pair.Value = config.pop('dlc.role.arn')
            request.Arguments.append(pair)
        
        if config:
            pair = models.KVPair()
            pair.Key = 'dlc.sql.set.config'
            values = []
            for key, value in config.items():
                values.append(f"set {key}={value}")

            pair.Value = base64.b64encode(';'.join(values).encode('utf8')).decode('utf8')
            request.Arguments.append(pair)
        
        
        response = self._DLC_CLIENT.CreateSparkSessionBatchSQL(request)
        return response.BatchId

    
    def get_statements_from_spark_batch(self, batch_id, convert=True):

        request = models.DescribeSparkSessionBatchSQLRequest()
        request.BatchId = batch_id

        response = self._DLC_CLIENT.DescribeSparkSessionBatchSQL(request)

        state = response.State

        if convert:
            state = constants.SparkBatchTaskStatus.toTaskStatus(state)

        return {
            'state': state,
            'tasks': response.Tasks,
            'message': response.Event
        }


    def get_statement_result_for_spark_batch(self, task_id):
        return self.get_statement_results_for_spark_batch([task_id])[task_id]

    
    def get_statement_results_for_spark_batch(self, task_ids):

        request = models.DescribeNotebookSessionStatementSqlResultRequest()

        task_set = {}
        for task_id in task_ids:
            request.TaskId = task_id
            response = self._DLC_CLIENT.DescribeNotebookSessionStatementSqlResult(request)

            task_set[task_id] = {
                'rowAffectInfo': '',
                'path': response.OutputPath,
            }
        return task_set


    def submit_statement(self, engine, engine_type, catalog, statement, database='', config={}):

        request = models.CreateTaskRequest()
        request.DataEngineName = engine
        request.DatasourceConnectionName = catalog
        request.Task = models.Task()
        request.DatabaseName = database

        task = models.SQLTask()
        task.SQL = base64.b64encode(statement.encode('utf8')).decode('utf8')
        task.Config = []

        for k, v in config.items():
            pair = models.KVPair()
            pair.Key = k
            pair.Value = str(v)
            task.Config.append(pair)


        if engine_type == constants.EngineType.SPARK:
            request.Task.SparkSQLTask = task
        else:
            request.Task.SQLTask = task

        response = self._DLC_CLIENT.CreateTask(request)

        return response.TaskId

    def get_statements(self, *statement_ids):
            
        request = models.DescribeTasksRequest()

        f = models.Filter()
        f.Name = "task-id"
        f.Values = statement_ids
        request.Filters = [f]

        response = self._DLC_CLIENT.DescribeTasks(request)

        task_set = {}

        for task in response.TaskList:
            task_set[task.Id] = {
                "rowAffectInfo": task.RowAffectInfo,
                "message": task.OutputMessage,
                "path" : task.OutputPath,
                "state": task.State,
            }
        return task_set
    
    def get_statement(self, statement_id):
        return self.get_statements(statement_id)[statement_id]
        
    def get_statement_results(self, statement_id, next=None):

        request = models.DescribeTaskResultRequest()
        request.TaskId = statement_id
        request.NextToken = next

        response = self._DLC_CLIENT.DescribeTaskResult(request)
        columns = []
        for schema in response.TaskInfo.ResultSchema:
            columns.append(to_column(schema))

        return {
            "state": response.TaskInfo.State,
            "sqlType": response.TaskInfo.SQLType,
            "message": response.TaskInfo.OutputMessage,
            "rowAffectInfo": response.TaskInfo.RowAffectInfo,
            "path": response.TaskInfo.OutputPath,
            "columns":columns,
            "results": json.loads(response.TaskInfo.ResultSet),
            "next": response.TaskInfo.NextToken
        }

    def get_lakefs_auth(self, url):
        request = DescribeLakeFsPathRequest()
        request._FsPath = url
        response = self._DLC_CLIENT.DescribeLakeFsPath(request)
        return {
            "secretId": urllib.parse.unquote(response._AccessToken._SecretId),
            "secretKey": urllib.parse.unquote(response._AccessToken._SecretKey),
            "token": urllib.parse.unquote(response._AccessToken._Token),
        }

    def object_exists(self, bucket, key):
        return self._COS_CLIENT.object_exists(bucket, key)

    def get_cos_object_stream(self, bucket, key):
        return self._COS_CLIENT.get_object(Bucket=bucket, Key=key)['Body'].get_raw_stream()

    def get_cos_object_stream_to_file(self, bucket, key, name):
        return self._COS_CLIENT.get_object(Bucket=bucket, Key=key)['Body'].get_stream_to_file(name)

    def iter_cos_objects(self, bucket, prefix):
        maker = ""
        while True:
            response = self._COS_CLIENT.list_objects(
                Bucket=bucket,
                Prefix=prefix,
                Marker=maker,
            )

            contents = response.get('Contents', [])

            for item in contents:

                key = item['Key'].strip('/')
                size = int(item['Size'])

                if item['Key'] == prefix or key.endswith('_SUCCESS') or size == 0:
                    # 过滤 parent 文件夹
                    # 过滤 _SUCCESS 文件
                    # 过滤 size == 0 对象
                    continue

                yield item

            if response['IsTruncated'] == 'false':
                break 
            maker = response['Marker']



def to_column(schema):
    return {
        "name": schema.Name,
        "type": schema.Type,
        "nullable": schema.Nullable == 'NULLABLE',
        "scale": schema.Scale,
        "precision": schema.Precision,
        "is_partition": schema.IsPartition,
        "comment": schema.Comment,
    }



class DescribeLakeFsPathRequest(models.AbstractModel):

    def __init__(self):
        self._FsPath = None
    
    def _deserialize(self, params):
        self._FsPath = params.get("FsPath")

class DescribeLakeFsPathResponse(models.AbstractModel):

    def __init__(self) -> None:
        self._RequestId = None
        self._AccessToken = None

    def _deserialize(self, params):
        
        if params.get("AccessToken") is not None:
            self._AccessToken =  LakeFileSystemToken()
            self._AccessToken._deserialize(params.get("AccessToken"))
        self._RequestId = params.get("RequestId")

class LakeFileSystemToken(models.AbstractModel):

    def __init__(self) -> None:

        self._SecretId = None
        self._SecretKey = None
        self._Token = None
        self._ExpiredTime = None
        self._IssueTime = None
    
    def _deserialize(self, params):
        self._SecretId = params.get("SecretId")
        self._SecretKey = params.get("SecretKey")
        self._Token = params.get("Token")
        self._ExpiredTime = params.get("ExpiredTime")
        self._IssueTime = params.get("IssueTime")


class WrappedDlcClient(dlc_client.DlcClient):

    RETRY_TIMES = 3

    def __init__(self, credential, region, profile=None):
        super().__init__(credential, region, profile)

    def DescribeLakeFsPath(self, request):
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLakeFsPath", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = DescribeLakeFsPathResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def call(self, action, params, options=None, headers=None):
        retry = 0

        err = None

        while retry < self.RETRY_TIMES:
            retry += 1
            try:
                body = super().call(action, params, options, headers)
                
                # hack error message
                r = json.loads(body)
                if 'Error' in r['Response'] and 'Detail' in r['Response']['Error']:

                    try:
                        o = json.loads(r['Response']['Error']['Detail'])
                        r['Response']['Error']['Message'] = o['errMsg']
                        return json.dumps(r)
                    except Exception as e:
                        LOG.warning(e)
                        r['Response']['Error']['Message'] = r['Response']['Error']['Detail']
                    
                return body
            # except TencentCloudSDKException as e:
            #     LOG.error(e)
            #     err = e
            #     if e.code in [errorcodes.RESOURCENOTFOUND_DATAENGINENOTFOUND, ]:
            #         retry = self.RETRY_TIMES
            except Exception as e:
                LOG.error(e)
                err = e

        if err is not None:
            raise err

        return body
            