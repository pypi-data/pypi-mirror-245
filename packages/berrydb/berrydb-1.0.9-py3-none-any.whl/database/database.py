import requests
import json
from urllib.parse import quote
from utils.utils import Utils
from constants.constants import debug_mode
from constants.constants import documents_url, query_url, document_by_id_url, bulk_upsert_documents_url, transcription_url, transcription_yt_url, caption_url, create_label_studio_project_url, import_label_studio_project_url, reimport_label_studio_project_url, couchbase_config

class Database:
    __api_key: str
    __bucket_name: str
    __database_id: int
    __database_name: str

    def __init__(
        self, api_key: str, bucket_name: str, database_id: int, database_name: str
    ):
        if api_key is None:
            Utils.print_error_and_exit("API Key cannot be None")
        if bucket_name is None:
            Utils.print_error_and_exit("Bucket name cannot be None")
        if database_id is None:
            Utils.print_error_and_exit("Database not found")
        self.__api_key = api_key
        self.__bucket_name = bucket_name
        self.__database_id = database_id
        self.__database_name = database_name

    def apiKey(self):
        return self.__api_key

    def bucketName(self):
        return self.__bucket_name

    def databaseId(self):
        return self.__database_id

    def databaseName(self):
        return self.__database_name

    def get_all_documents(self):
        """Function summary

        Args:
            No Arguments

        Returns:
            list: List of Documents
        """

        url = documents_url
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseId": self.__database_id,
        }

        if debug_mode:
            print("url:", url)
            print("params:", params)

        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            if debug_mode:
                print("documents result ", response.json())
            return json.loads(response.text)
        except Exception as e:
            print("Failed to fetch document: {}".format(str(e)))
            return []

    def get_all_documents_with_col_filter(self, col_filter=["*"]):
        """Function summary

        Args:
            arg1 (list<str>): Column list (Optional)

        Returns:
            list: List of Documents
        """

        url = documents_url
        """ params = {
            "columns": col_filter,
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseId": self.__database_id,
        } """
        url += "?apiKey=" + self.__api_key
        url += "&bucket=" + self.__bucket_name
        url += "&databaseId=" + str(self.__database_id)
        url += "&columns=" + (",".join(col_filter))

        if debug_mode:
            print("url:", url)
        try:
            response = requests.get(url)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            if debug_mode:
                print("documents result ", response.json())
            # return response.json()
            return json.loads(response.text)
        except Exception as e:
            print("Failed to fetch document: {}".format(str(e)))
            return []

    def get_document_by_object_id(
        self,
        document_id,
        key_name=None,
        key_value=None,
    ):
        """Function summary

        Args:
            arg1 (str): Document Key/Id
            arg2 (str): Key Name (optional)
            arg3 (str): Key Value (optional)

        Returns:
            list: List of Documents
        """

        url = document_by_id_url.format(quote(document_id))
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseId": self.__database_id,
        }

        if document_id is not None:
            params["docId"] = document_id
        if key_name is not None:
            params["keyName"] = key_name
        if key_value is not None:
            params["keyValue"] = key_value

        if debug_mode:
            print("url:", url)
            print("params:", params)

        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            jsonRes = response.json()
            if debug_mode:
                print("docById result ", jsonRes)
            return jsonRes
        except Exception as e:
            print("Failed to fetch document by id {} : {}".format(document_id, str(e)))
            return ""


    def query(self, query: str):
        """Function summary

        Args:
            arg1 (str): Query String

        Returns:
            list: List of Documents
        """

        url = query_url
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseId": self.__database_id,
        }
        payload = query

        if debug_mode:
            print("url:", url)
            print("query:", query)
            print("params:", params)
        headers = Utils.get_headers(self.__api_key)

        try:
            response = requests.post(url, data=payload, headers=headers, params=params)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            if debug_mode:
                print("query result ", response.json())
            return json.loads(response.text)
        except Exception as e:
            print("Failed to query : {}".format(str(e)))
            return ""

    def __upsert(self, documents) -> str:
        url = bulk_upsert_documents_url
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseId": self.__database_id,
        }

        payload = json.dumps(documents)
        if debug_mode:
            print("url:", url)
            print("payload:", payload)
        headers = Utils.get_headers(self.__api_key)

        try:
            response = requests.post(url, data=payload, headers=headers, params=params)
            if response.status_code != 200:
                try:
                    resp_content = response.json()
                except ValueError:
                    resp_content = response.text
                Utils.handleApiCallFailure(resp_content, response.status_code)
            if debug_mode:
                print("upsert result ", response)
            return response.text
        except Exception as e:
            print("Failed to upsert document: {}".format(str(e)))
            return ""

    def upsert(self, documents) -> str:
        """Function summary

        Args:
            arg1 (str): List of documents Object to add/update (Each document should have a key 'id' else a random string is assigned)

        Returns:
            str: Success/Failure message
        """
        try:
            if type(documents) != list:
                documents = [documents]
            return self.__upsert(documents)
        except Exception as e:
            print("Failed to upsert documents: {}".format(str(e)))
            return ""

    def upsert_document(self, documents) -> str:
        """(DEPRECATED)
        Function summary

        Args:
            arg1 (str): List of documents Object to add/update (Each document should have a key 'id' else a random string is assigned)

        Returns:
            str:  Success/Failure message
        """

        print("upsert_document is deprecated, please use upsert instead.")
        return ""

    def deleteDocument(self, document_id):
        """Function summary

        Args:
            arg1 (str): Document Data Object to delete a document by id

        Returns:
            str: Success message
        """

        url = document_by_id_url.format(quote(document_id))
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseId": self.__database_id,
        }

        if debug_mode:
            print("url:", url)
            print("params:", params)

        try:
            response = requests.delete(url, params=params)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            jsonRes = response.text
            if debug_mode:
                print("Delete document result ", jsonRes)
            return jsonRes
        except Exception as e:
            print(
                "Failed to delete document by id {}, reason : {}".format(
                    document_id, str(e)
                )
            )
            return ""

    def transcribe(self, video_url: str):
      url = transcription_url

      body = {
        "url": video_url,
      }

      payload = json.dumps(body)
      if debug_mode:
          print("url:", url)
          print("payload:", payload)
      headers = Utils.get_headers(self.__api_key)

      try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code != 200:
          Utils.handleApiCallFailure(response.json(), response.status_code)
        res = response.text
        if debug_mode:
          print("Transcription result: ", res)
        return res
      except Exception as e:
        print(f"Failed to get transcription for the url {video_url}, reason : {str(e)}")
        return ""


    def transcribeYT(self, video_url: str):

      url = transcription_yt_url

      body = {
        "url": video_url,
      }

      payload = json.dumps(body)
      if debug_mode:
          print("url:", url)
          print("payload:", payload)
      headers = Utils.get_headers(self.__api_key)

      try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code != 200:
          Utils.handleApiCallFailure(response.json(), response.status_code)
        res = response.text
        if debug_mode:
          print("Youtube transcription result: ", res)
        return res
      except Exception as e:
        print(f"Failed to get transcription for the youtube url {video_url}, reason : {str(e)}")
        return ""

    def caption(self, image_url: str):
      url = caption_url

      body = {
        "url": image_url,
      }

      payload = json.dumps(body)
      if debug_mode:
        print("url:", url)
        print("payload:", payload)
      headers = Utils.get_headers(self.__api_key)

      try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code != 200:
          Utils.handleApiCallFailure(response.json(), response.status_code)
        res = response.text
        if debug_mode:
          print("Caption result: ", res)
        return res
      except Exception as e:
        print(f"Failed to get caption for the url {image_url}, reason : {str(e)}")
        return ""

    def embed(self, open_ai_api_key, embedding_function = None, limit = None):
        """Function summary

        Args:
            arg1 (str): OpenAI API key to embed the database

        Returns:
            str: An instance of the Embeddings class
        """
        from embeddings.embeddings import Embeddings
        embeddings = Embeddings(
          self.__database_id,
          self.__database_name,
          self.__bucket_name,
          self.__api_key,
          open_ai_api_key,
          limit,
          embedding_function
        )
        return embeddings.embedDb()

    def ask_and_get_answers(self, open_ai_api_key, question, k=3):
        """Function summary

        Args:
            arg1 (str): OpenAI API key to embed the database
            arg2 (str): Query/Question to for your database
            arg3 (str): K value (optional)

        Returns:
            str: An instance of the Embeddings class
        """

        from embeddings.embeddings import Embeddings
        embeddings = Embeddings(
          self.__database_id,
          self.__database_name,
          self.__bucket_name,
          self.__api_key,
          open_ai_api_key,
        )
        return embeddings.ask_and_get_answers(question, k)