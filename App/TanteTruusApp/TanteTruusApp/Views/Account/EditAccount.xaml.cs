using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using TanteTruusApp.Helpers;
using Xamarin.Essentials;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace TanteTruusApp.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class EditAccount : ContentPage
    {
        public EditAccount(string _name, DateTime _birthdate, string _email)
        {
            InitializeComponent();
            NameEntry.Text = _name;
            EmailEntry.Text = _email;
            DateField.Date = _birthdate;
        }

        public async void UpdateUser(object sender, EventArgs e)
        {
            if(PasswordEntry.Text == PasswordEntry2.Text && !String.IsNullOrEmpty(PasswordEntry.Text))
            {
                string name = NameEntry.Text;
                string email = EmailEntry.Text;
                string password = PasswordEntry.Text;
                string date = DateField.Date.ToString("dd/MM/yyyy");

                string user_uuid = Preferences.Get("uuid", null);
                if (user_uuid != null)
                {
                    if (!String.IsNullOrWhiteSpace(email) || !String.IsNullOrWhiteSpace(password))
                    {
                        List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                        req.Add(new KeyValuePair<string, string>("uuid", user_uuid));
                        req.Add(new KeyValuePair<string, string>("name", name));
                        req.Add(new KeyValuePair<string, string>("email", email));
                        req.Add(new KeyValuePair<string, string>("password", password));
                        req.Add(new KeyValuePair<string, string>("birthdate", date));

                        Response res = await http_request.MakePostRequest("user/update", req);
                        JToken data = res.ResponseData;

                        if (res.IsSuccess)
                        {
                            await Navigation.PopAsync();
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
                    Preferences.Set("uuid", null);
                    await Navigation.PushModalAsync(new MainPage());
                }
            }
            else
            {
                error.Text = "Passwords do not match.";
            }
        }
    }
}