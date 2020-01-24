using Newtonsoft.Json.Linq;

public class Response
    {
        public bool IsSuccess = false;
        public string Message;
        public JToken ResponseData;

        public Response(bool status, JToken data=null, string message = null)
        {
            IsSuccess = status;
            Message = message;
            ResponseData = data;
        }
    }
