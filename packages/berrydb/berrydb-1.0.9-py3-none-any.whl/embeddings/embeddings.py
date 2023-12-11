import os
import tiktoken
import faiss
import numpy as np
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.docstore.in_memory import InMemoryDocstore

from database.database import Database
from constants.constants import debug_mode
from utils.utils import Utils
from loaders.berrydb_json_loader import BerryDBJSONLoader

class Embeddings:
  __berry_db_api_key: str
  __open_ai_api_key: str
  __bucket_name: str
  __database_id: str
  __database_name: str
  __embedding_function: str
  __limit: str

  def __init__(
    self,
    database_id: int,
    database_name: str,
    bucket_name: str,
    berry_db_api_key: str,
    open_ai_api_key: str,
    limit: int = None,
    embedding_function = None,
  ):
      if not database_id:
        Utils.print_error_and_exit("Database cannot be None")
      if not database_name:
        Utils.print_error_and_exit("Database name cannot be None")
      if not bucket_name:
        Utils.print_error_and_exit("Bucket name cannot be None")
      if not berry_db_api_key:
        Utils.print_error_and_exit("API Key cannot be None")
      if not open_ai_api_key:
        Utils.print_error_and_exit("OpenAI API Key cannot be None")
      if limit and not (isinstance(limit, int) and int(limit) > 0):
        Utils.print_error_and_exit("Limit should be none or a positive integer")

      self.__berry_db_api_key = berry_db_api_key
      self.__open_ai_api_key = open_ai_api_key
      self.__bucket_name = bucket_name
      self.__database_id = database_id
      self.__database_name = database_name
      self.__embedding_function = embedding_function
      self.__limit = int(limit) if limit else None


  def embedDb(self):
      if debug_mode:
        print("self.__database_id: ", self.__database_id)
        print("self.__database_name: ", self.__database_name)
        print("self.__bucket_name: ", self.__bucket_name)
        print(f"Checking if you have access to {self.__database_name}")

      documents = []
      records = self.__get_all_records_for_database()
      records = [item["BerryDb"] for item in records]
      if self.__limit:
        records = records[: self.__limit]
      if debug_mode:
        print(f"Fetched {len(records)} records")
      if len(records) <= 0:
        Utils.print_error_and_exit("Database does not have any records")


      documents = self.__load_JSON(records)

      tokens, embedding_cost = self.__calculate_embedding_cost(documents)
      if debug_mode:
        print(f'Embedding Cost: ${embedding_cost:.4f}')
        print(f'Number of chunks: {len(documents)}')

      return self.__embed_docs(documents, True, self.__embedding_function)

  def ask_and_get_answers(self, q, k=3):
    llm = ChatOpenAI(
      model="gpt-3.5-turbo", temperature=1, openai_api_key=self.__open_ai_api_key
    )
    v_store = self.__get_vector_store()
    retriever = v_store.as_retriever(search_kwargs={"k": k})
    chain = RetrievalQA.from_chain_type(
      llm=llm, chain_type="stuff", retriever=retriever
    )
    answer = chain.run(q)
    if debug_mode:
      print("answer: ", answer)
    return answer

  def __get_embeddings_from_docs(self, texts, open_ai_api_key):
    return OpenAIEmbeddings(openai_api_key=open_ai_api_key)

  def __get_vector_store(self):
    if not self.is_embedded():
      Utils.print_error_and_exit(f"Database with name {self.__database_name} is not embedded. Please embed the database and try again.")
    records = self.__get_all_records_for_database()
    records = [item["BerryDb"] for item in records]
    docs = self.__load_JSON(records)
    vector_store = self.__embed_docs(docs)
    return vector_store

  def __embed_docs(
    self,
    documents,
    generate_embeddings = False,
    embedding_function = None,
  ):
    if embedding_function and not callable(embedding_function):
      Utils.print_error_and_exit("Embedding Function must be a function or None")

    texts = [d.page_content for d in documents]
    metadatas = [d.metadata for d in documents]

    if embedding_function:
      return embedding_function(documents)

    embedding = self.__get_embeddings_from_docs(texts, self.__open_ai_api_key)

    if generate_embeddings:
      # self.get_embeddings_from_docs(generate_embeddings, embedding_function)
      embeddings = embedding.embed_documents(texts)
      index = faiss.IndexFlatIP(len(embeddings[0]))
      vector = np.array(embeddings, dtype=np.float32)
      index.add(vector)
    else:
      try:
        embeddings_file_path = self.__get_embeddings_path(self.__database_id, self.__database_name)
        if debug_mode:
          print("embeddings_file_path: ", embeddings_file_path)
        vector = np.load(embeddings_file_path)
        index = faiss.IndexFlatIP(len(vector[0]))
        index.add(vector)
      except:
        Utils.print_error_and_exit(f"Database with name {self.__database_name} is not embedded. Please embed the database and try again.")

    documents = []

    for i, text in enumerate(texts):
      metadata = metadatas[i] if metadatas else {}
      documents.append(Document(page_content=text, metadata=metadata))
    index_to_docstore_id = {i: doc.metadata['objectId'] for i, doc in enumerate(documents)}
    if debug_mode:
      print('index to doctore map')
      print(index_to_docstore_id)
    docstore = InMemoryDocstore(
        {index_to_docstore_id[i]: doc for i, doc in enumerate(documents)}
    )

    faiss_vector_store = FAISS(embedding.embed_query, index, docstore, index_to_docstore_id)

    if generate_embeddings:
      file_path = self.__get_embeddings_path(self.__database_id, self.__database_name)
      doc_store_id_to_index = {index_to_docstore_id[i]: i for i in range(len(index_to_docstore_id))}
      if debug_mode:
        print(doc_store_id_to_index)
      self.__persist_embeddings(file_path, vector)
      self.__store_embedding_data(file_path, doc_store_id_to_index)

    return faiss_vector_store;

  def __get_embeddings_path(self, database_id, database_name):
    embeddings_file_path_prefix = os.environ.get("EMBEDDINGS_FILE_PATH_PREFIX", None)
    if debug_mode:
      print("embeddings_file_path_prefix: ", embeddings_file_path_prefix)
    return f"{embeddings_file_path_prefix if embeddings_file_path_prefix else ''}{str(database_id)}_{database_name}_embeddings.npy"


  def __persist_embeddings(self, file_path, embeddings):
    # Convert embeddings to a NumPy array and persist to file system
    embeddings_array = np.array(embeddings)
    np.save(file_path, embeddings_array)

  def __store_embedding_data(
    self, file_path, mappings
  ):
    data = {
      'databaseId': self.__database_id,
      "path": file_path,
      "mappings": mappings,
    }
    doc = {"id": str(self.__database_id) + "_" + self.__database_name, "data": data}

    self.__upsert_file_path_data_into_vector_bucket(doc)

  def __calculate_embedding_cost(self, texts):
    enc = tiktoken.encoding_for_model("text-embedding-ada-002")
    total_tokens = sum([len(enc.encode(page.page_content)) for page in texts])
    return total_tokens, total_tokens / 1000 * 0.0004
    # return len(texts), 0

  def __get_all_records_for_database(self):
    db = Database(self.__berry_db_api_key, self.__bucket_name, self.__database_id, self.__database_name)
    records = db.get_all_documents()
    if debug_mode:
      print(f"A total of {len(records)} fetched")
      print(records)
    return records

  def __load_JSON(self, records):
    # loader = BerryDBJSONCSVLoader(json_data=records, text_content=False)
    loader = BerryDBJSONLoader(
        json_data=records, jq_schema=".[]", text_content=False
    )
    return loader.load()

  def __upsert_file_path_data_into_vector_bucket(self, data):
    berryDb_vectors_bkt = Database(self.__berry_db_api_key, "Vectors", self.__database_id, self.__database_name,)
    berryDb_vectors_bkt.upsert_document(data)

  def is_embedded(self):
    berryDb_vectors = Database(self.__berry_db_api_key, "Vectors", self.__database_id, self.__database_name)
    # query = f'Select * from Vectors where databaseId = {db_id}'
    query = f"SELECT COUNT(*) AS count FROM `Vectors` WHERE databaseId = '{self.__database_id}'"
    result = berryDb_vectors.query(query)
    if debug_mode:
      print("result: ", result)
    try:
        count = result[0]["count"]
    except:
        count = 0
    return bool(count)