"""BASE WRITER MODULE"""

# pylint: disable=too-few-public-methods, no-member, too-many-arguments
from abc import ABC, abstractmethod
import json
import csv
import gzip
import time
from io import BytesIO
from pathlib import Path
from typing import Union, Any, List, Dict, Optional, Tuple
import boto3
from googleapiclient import discovery
from google.oauth2 import service_account


class Authenticator(ABC):
    """Interface for Resource Authentication"""

    def authenticate(self, configs: Optional[Dict[str, Any]]):
        """
        class method that does the actual authentication

        Raises:
            NotImplementedError: method must be overriden by subclasses

        Returns:
            None : has no return value
        """
        print(configs)
        return True


class BaseResourceWriter(ABC):
    """Interface class for resource writers"""

    @abstractmethod
    def write_to_destination(self, write_path: str, data: Any) -> None:
        """Method to write data to final destination resource

        Args:
            write_path (str): string of the path to write the data
            data (Any): the data object to be written

        Raises:
            NotImplementedError: should be implemented by the child classes

        Returns:
            None : has no return
        """
        raise NotImplementedError

    def delete_destination(self, delete_path: str) -> None:
        """Method to delete from the destination

        Args:
            delete_path (str): path to delete

        Raises:
            KeyError: if givne delete path does not exist
            exc: _description_
            NotImplementedError: _description_
            NotImplementedError: _description_

        Returns:
            Union[Error|PrintMessage]: Either raises KeyError or print results
        """
        print(f"Not yet implemented to delete {delete_path}")


class AWSProfileAuthenticator(Authenticator):
    """Authenticator class for AWS Using AWS Profile"""

    def authenticate(self, configs: Optional[Dict[str, Any]] = None):
        """Authentication into AWS S3"""
        if configs is None:
            configs = {"profile_name": None}
        if configs.get("profile_name") is not None:
            boto3_session = boto3.Session(profile_name=configs["profile_name"])
        else:
            boto3_session = boto3.Session()

        return boto3_session.resource("s3")


class GCPServiceAccountAuthenticator(Authenticator):
    """Ayuthenticator class for GCP Using Service Account"""

    def authenticate(self, configs: Dict[str, Any]):
        """Authentication into Google Cloud"""
        if configs.get("service_account_info") is not None:
            credentials = service_account.Credentials.from_service_account_info(
                info=configs["service_account_info"]
            )
        elif configs.get("service_account_file") is not None:
            credentials = service_account.Credentials.from_service_account_file(
                filename=configs["service_account_file"]
            )
        else:
            raise KeyError(
                "missing service account file or info (dict) for authentication"
            )

        service = discovery.build("storage", "v1", credentials=credentials)
        return service


class LocalAuthenticator(Authenticator):
    """Placeholder classs for Local Authentication"""

    def authenticate(self, configs: Optional[Dict[str, Any]]):
        return True


class AWSS3JSONWriter(BaseResourceWriter):
    """Base Writer Class for S3 Destination"""

    def __init__(
        self,
        bucket: str,
        configs: Dict[str, Any],
        authenticator=AWSProfileAuthenticator,
    ):

        self.bucket: str = bucket
        self.configs: Optional[Dict[str, Any]] = configs
        self.resource = authenticator().authenticate(self.configs)

    def write_to_destination(self, write_path: str, data: Any) -> None:

        """Writes Data To JSON in S3 Generally expects a List, Dictionary
        Args:
            payload (Union[List[Dict[Any, Any]], Dict[Any, Any], Any]): can be any python data type

        Retruns:
            Tuple(Str,List[Dict[Any,Any]]): write_path full s3 path of object to be written
                                            data a list of dictionaries having the data
        """

        write_path = f"{write_path}.json"
        self.resource.Object(self.bucket, write_path).put(
            Body=json.dumps(data, indent=2)
        )
        print(f"done writting data to s3://{self.bucket}/{write_path}")

    def delete_destination(self, delete_path: str) -> None:
        """Method to delete from the destination

        Args:
            delete_path (str): path to delete

        Raises:
            KeyError: if givne delete path does not exist
        Returns:
            Union[Error|PrintMessage]: Either raises KeyError or print results
        """
        bucket = self.resource.Bucket(self.bucket)
        try:
            print(
                "5 seconds before you delete all records in the path\n\n"
                f"s3://{self.bucket}/{delete_path}\n\n"
            )
            time.sleep(5)
            deletes = bucket.objects.filter(Prefix=delete_path).delete()
            files = [row["Key"] for item in deletes for row in item["Deleted"]]
            print(f"deleted records are \n{files}\n")
        except Exception as exc:
            raise exc


class GCPCloudStorageJSONWriter(BaseResourceWriter):
    """Base Writer Class for GCP Cloud Storage Destination"""

    def __init__(
        self,
        bucket: str,
        configs: Dict[str, Any],
        authenticator=GCPServiceAccountAuthenticator,
    ):

        self.bucket: str = bucket
        self.configs: Dict[str, Any] = configs
        self.resource = authenticator().authenticate(self.configs)

    def write_to_destination(self, write_path: str, data: Any) -> None:

        """Writes Data To JSON in GCP Cloud Storage Generally expects a List, Dictionary"""

        write_path = f"{write_path}.json"
        self.resource.objects().insert(
            bucket=self.bucket, body=data, media_body=write_path
        ).execute()
        print(f"done writting data to gs://{self.bucket}/{write_path}")


class AWSS3JSONGZIPWriter(BaseResourceWriter):

    """AWS GZIP Writer"""

    def __init__(
        self,
        bucket: str,
        configs: Optional[Dict[str, Any]] = None,
        authenticator=AWSProfileAuthenticator,
    ):
        self.bucket: str = bucket
        self.configs = configs
        self.resource = authenticator().authenticate(self.configs)

    def write_to_destination(self, write_path: str, data: Any) -> None:
        gz_body = BytesIO()
        gz_file = gzip.GzipFile(None, "wb", 7, gz_body)
        gz_file.write(json.dumps(data).encode("utf-8"))
        gz_file.close()

        write_path = f"{write_path}.json.gz"

        self.resource.Bucket(self.bucket).put_object(
            Key=write_path,
            ContentEncoding="gzip",
            Body=gz_body.getvalue(),
        )
        print(f"done writting data to s3://{self.bucket}/{write_path}")

    def delete_destination(self, delete_path: str) -> None:
        """Method to delete from the destination

        Args:
            delete_path (str): path to delete

        Raises:
            KeyError: if givne delete path does not exist
        Returns:
            Union[Error|PrintMessage]: Either raises KeyError or print results
        """
        bucket = self.resource.Bucket(self.bucket)
        try:
            print(
                "5 seconds before you delete all records in the path\n\n"
                f"s3://{self.bucket}/{delete_path}\n\n"
            )
            time.sleep(5)
            deletes = bucket.objects.filter(Prefix=delete_path).delete()
            files = [row["Key"] for item in deletes for row in item["Deleted"]]
            print(f"deleted records are \n{files}\n")
        except Exception as exc:
            raise exc


class LocalJSONWriter(BaseResourceWriter):
    """Writer Class for Local Directories"""

    def __init__(
        self,
        bucket: str,
        configs: Optional[Dict[str, Any]] = None,
        authenticator=LocalAuthenticator,
    ):
        self.bucket: str = bucket
        self.configs = configs
        self.resource = authenticator().authenticate(self.configs)

    def write_to_destination(self, write_path: str, data: Any) -> None:
        full_path = write_path.rsplit("/", maxsplit=1)[0]
        Path(f"{self.bucket}/{full_path}").mkdir(parents=True, exist_ok=True)

        write_path = f"{write_path}.json"

        with open(
            f"{self.bucket}/{write_path}", mode="w", encoding="utf8"
        ) as dest_file:
            json.dump(data, dest_file, indent=4)
            print(f"done writting data to {self.bucket}/{write_path}")

    def delete_destination(self, delete_path: str) -> None:
        delete_path = f"{self.bucket}/{delete_path}"
        files = Path(f"{delete_path}").glob("*.*")
        files = list(files)
        print("5 seconds before you delete all records in the path\n" f"{delete_path}")
        time.sleep(5)
        _ = [file.unlink(missing_ok=True) for file in files]


class LocalCSVWriter(BaseResourceWriter):
    """Writer Class for Local CSV"""

    def __init__(
        self,
        bucket: str,
        configs: Optional[Dict[str, Any]] = None,
        authenticator=LocalAuthenticator,
    ):
        self.bucket: str = bucket
        self.configs = configs
        self.resource = authenticator().authenticate(self.configs)

    def write_to_destination(self, write_path: str, data: Any) -> None:
        full_path = write_path.rsplit("/", maxsplit=1)[0]
        Path(f"{self.bucket}/{full_path}").mkdir(parents=True, exist_ok=True)

        write_path = f"{write_path}.csv"
        field_names = list(data[0].keys())

        with open(f"{self.bucket}/{write_path}", mode="w", encoding="utf8") as myfile:
            writer = csv.DictWriter(
                myfile, fieldnames=field_names, quoting=csv.QUOTE_ALL
            )
            writer.writeheader()
            writer.writerows(data)
            print(f"done writting data to {self.bucket}/{write_path}")


class BaseWriter(ABC):
    """ "Normal Base Writer Class"""

    success: List[bool] = []

    def __init__(
        self,
        bucket: str,
        folder_path: str,
        destination: str,
        configs: Optional[Dict[str, Any]] = None,
        clear_destination: bool = False,
    ):
        self.bucket = bucket
        self.folder_path = folder_path
        self.destination = destination
        self.configs = configs
        self.resource = self._get_resource()
        self.clear_destination: bool = clear_destination
        self.current_destination: Union[str, None] = None

    def _get_resource(self) -> BaseResourceWriter:
        """Gets the appropriate WriterResource"""
        resource_writers = {
            "aws_s3_json": AWSS3JSONWriter,
            "gcp_cloudstorage_json": GCPCloudStorageJSONWriter,
            "local_json": LocalJSONWriter,
            "local_csv": LocalCSVWriter,
            "aws_s3_json_gzip": AWSS3JSONGZIPWriter,
        }
        if self.destination not in resource_writers:
            raise NotImplementedError(
                f"writer destination is wrong! allowed values: \n{list(resource_writers.keys())}"
            )
        resource = resource_writers[self.destination](self.bucket, self.configs)
        return resource

    def write_data(self, payload: Any):
        """Base Write Method to Destination"""
        write_path, data = self.verify_data(payload)
        delete_path = write_path.rsplit("/", maxsplit=1)[0].strip()

        if not data:
            self.not_success()
            return

        if (self.clear_destination is True) and (
            self.current_destination != delete_path
        ):
            self.resource.delete_destination(delete_path=delete_path)
            self.current_destination = delete_path
        self.resource.write_to_destination(write_path, data)
        self.is_success()

    def is_success(self) -> None:
        """Append True to the Success List Object"""
        self.success.append(True)

    def not_success(self) -> None:
        """Append False to the Success List Object"""
        self.success.append(False)

    @abstractmethod
    def verify_data(
        self, payload: Union[List[Dict[Any, Any]], Dict[Any, Any], Any]
    ) -> Tuple[str, Union[List[Dict[Any, Any]], Dict[Any, Any], Any]]:

        """Used to verify data is properly formatted and we have expected fields

        Args:
            payload (Union[List[Dict[Any, Any]], Dict[Any, Any], Any]): can be any python data type

        Raises:
            NotImplementedError: _description_

        Returns:
            Tuple[str, Union[List[Dict[Any, Any]], Dict[Any, Any], Any]]: write_path and data itself
        """
        raise NotImplementedError
