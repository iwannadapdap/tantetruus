using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using TanteTruusApp.Helpers;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace TanteTruusApp.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class RegisterPage : ContentPage
    {
        public RegisterPage()
        {
            InitializeComponent();
        }

        private async void Register(object sender, EventArgs e)
        {
            if (password_field.Text == password_field2.Text && !String.IsNullOrEmpty(password_field.Text))
            {
                string name = name_field.Text;
                string email = email_field.Text;
                string password = password_field.Text;
                string date = date_field.Date.ToString("dd/MM/yyyy");

                if (!String.IsNullOrWhiteSpace(email) || !String.IsNullOrWhiteSpace(password))
                {
                    List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                    req.Add(new KeyValuePair<string, string>("name", name));
                    req.Add(new KeyValuePair<string, string>("email", email));
                    req.Add(new KeyValuePair<string, string>("password", password));
                    req.Add(new KeyValuePair<string, string>("birthdate", date));

                    Response res = await http_request.MakePostRequest("auth/register", req);
                    JToken data = res.ResponseData;

                    if (res.IsSuccess)
                    {
                        await Navigation.PushModalAsync(new LoginPage());
                    }
                    else
                    {
                        await DisplayAlert("Error", res.ResponseData.Value<string>(), "OK");
                    }
                }
                else
                {
                    error.Text = "Please fill out valid info in all fields";
                }
            }
            else
            {
                error.Text = "Passwords don't match";
            }
        }
    }
}