debug_mode = True

# BerryDB Base URLs
base_url = "https://app.berrydb.io"
berry_gpt_base_url = "http://gpt.berrydb.io:9090"
label_studio_base_url = "https://app.berrydb.io:8080"

# Profile service endpoints
get_schema_id_url = base_url + "/profile/schema"
get_database_id_url = base_url + "/profile/database"
create_database_url = base_url + "/profile/database"
get_database_list_by_api_key_url = base_url + "/profile/database/list-by-api-key"

# Label Studio endpoints
create_label_studio_project_url = label_studio_base_url + "/api/projects"
setup_label_config_url = label_studio_base_url + "/api/projects/{}"
import_label_studio_project_url = label_studio_base_url + "/api/projects/{}/import?commit_to_project=false"
reimport_label_studio_project_url = label_studio_base_url + "/api/projects/{}/reimport"
couchbase_config = "cluster_ip=13.126.134.203;cluster_username=Admin;cluster_password=123456;bucket=BerryDb;scope={};collection=bObject"
create_annotations_url = label_studio_base_url + "/api/tasks/{}/annotations?project={}"
create_predictions_url = label_studio_base_url + "/api/predictions"

# Berrydb service endpoints
documents_url = base_url + "/berrydb/documents"
query_url = base_url + "/berrydb/query"
document_by_id_url = base_url + "/berrydb/documents/{}"
bulk_upsert_documents_url = base_url + "/berrydb/documents/bulk"

# ML backend endpoint
transcription_url = berry_gpt_base_url + "/transcription"
transcription_yt_url = berry_gpt_base_url + "/transcription-yt"
caption_url = berry_gpt_base_url + "/caption"

generic_error_message = "Oops! something went wrong. Please try again later."

# Default variables
default_bucket = "BerryDb"