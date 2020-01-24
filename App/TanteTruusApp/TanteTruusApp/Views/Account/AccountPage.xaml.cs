using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Xamarin.Essentials;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;
using TanteTruusApp.Models;
using TanteTruusApp.Helpers;

namespace TanteTruusApp.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class AccountPage : ContentPage
    {
        private User Current_user { get; set; }
        public AccountPage()
        {
            InitializeComponent();
        }

        protected override async void OnAppearing()
        {
            Current_user = await getUserData();

            Name.Text = $"Name: {Current_user.Name}";
            Email.Text = $"Email: {Current_user.Email}";
            Age.Text = $"Age: {Current_user.Age.ToString()}";
            Created_at.Text = $"Created at: {Current_user.Created_at}";
            Last_login.Text = $"Last login: {Current_user.Last_login}";

        }

        private async Task<User> getUserData()
        {
            string user_uuid = Preferences.Get("uuid", null);
            if (user_uuid != null)
            {
                User new_user = new User();
                List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                req.Add(new KeyValuePair<string, string>("uuid", user_uuid));

                Response res = await http_request.MakePostRequest("user/get", req);
                if (res.IsSuccess)
                {
                    JObject data = JObject.Parse(res.ResponseData.ToString());

                    string name = data["name"].Value<string>();
                    string email = data["email"].Value<string>();
                    string birthdate = data["birthdate"].Value<string>();
                    string created_at = data["created_at"].Value<string>();
                    string last_login = data["last_login"].Value<string>();

                    new_user = new User(name, email, birthdate, created_at, last_login);
                    return new_user;
                }
                Preferences.Set("uuid", null);
                await Navigation.PushModalAsync(new MainPage());
                return null;
            }
            throw new ArgumentException("UUID is not set");
        }

        public async void LogOut(object sender, EventArgs e)
        {
            Preferences.Set("uuid", null);
            await Navigation.PushModalAsync(new MainPage());
        }

        public async void EditAccount(object sender, EventArgs e)
        {
            await Navigation.PushAsync(new EditAccount(Current_user.Name, Current_user.Birthdate, Current_user.Email));
        }
    }
}