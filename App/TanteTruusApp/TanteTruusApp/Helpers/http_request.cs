using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;

namespace TanteTruusApp.Helpers
{
    class http_request
    {
        public static async Task<Response> MakePostRequest(string url_extention, List<KeyValuePair<string, string>> data)
        {
            HttpClient client = new HttpClient();

            client.BaseAddress = new Uri("34.131.166.34:5000/");

            HttpContent content = new FormUrlEncodedContent(data);
            content.Headers.ContentType = new MediaTypeHeaderValue("application/x-www-form-urlencoded");

            var result = await client.PostAsync(url_extention, content);
            try
            {
                string raw_result;
                JObject json;

                raw_result = await result.Content.ReadAsStringAsync();

                if (result.IsSuccessStatusCode)
                {
                    json = JObject.Parse(raw_result);
                    if ((bool)json["success"])
                    {
                        Console.WriteLine("succes =====================================");
                        return new Response(true, json["data"]);
                    }
                    else
                    {
                        Console.WriteLine("error =====================================");
                        return new Response(false, json["error"]);
                    }
                }
                else
                {
                    Console.WriteLine("Response failed =====================================");
                    return new Response(false);
                }
            }
            catch (Exception e)
            {
                throw new Exception("Can't read response: " + e);
            };
        }
        public static async Task<Response> MakeGetRequest(string url_extention)
        {
            HttpClient client = new HttpClient();

            client.BaseAddress = new Uri("34.131.166.34:5000/");

            var result = await client.GetAsync(url_extention);
            try
            {
                string raw_result;
                JObject json;

                raw_result = await result.Content.ReadAsStringAsync();

                if (result.IsSuccessStatusCode)
                {
                    json = JObject.Parse(raw_result);
                    if ((bool)json["success"])
                    {
                        Console.WriteLine("succes =====================================");
                        return new Response(true, json["data"]);
                    }
                    else
                    {
                        Console.WriteLine("error =====================================");
                        return new Response(false, json["error"]);
                    }
                }
                else
                {
                    Console.WriteLine("Response failed =====================================");
                    return new Response(false);
                }
            }
            catch (Exception e)
            {
                throw new Exception("Can't read repsonse: " + e);
            };
        }
    }
}
