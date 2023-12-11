from constants.constants import generic_error_message

class Utils:
  @classmethod
  def get_headers(self, api_key: str, content_type: str = "application/json"):
    return {"Content-Type": content_type, "x-api-key": api_key, "Accept": "*/*"}

  @classmethod
  def handleApiCallFailure(self, res, status_code):
    if status_code == 401:
      self.__print_error_and_exit(
        "You are Unauthorized. Please check your API Key"
      )
    if res.get("errorMessage", None):
      errMsg = res["errorMessage"]
    else:
      errMsg = generic_error_message if (res == None or res == "") else res
    raise Exception(errMsg)

  @classmethod
  def print_error_and_exit(self, msg=None):
    msg = msg if msg is not None else generic_error_message
    print(msg)
    raise Exception(msg)
    # exit()
