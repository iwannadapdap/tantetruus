using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Windows.Input;
using Xamarin.Essentials;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;
using TanteTruusApp.Helpers;

namespace TanteTruusApp.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class LoginPage : ContentPage
    {
        public LoginPage()
        {
            InitializeComponent();
            NavigationPage.SetHasNavigationBar(this, false);
        }

        public async void login_button_click(object sender, EventArgs e)
        {
            string email = loginid.Text;
            string password = passid.Text;
            string installId = Preferences.Get("FcmKey", null);

            if (installId != null)
            {
                if (!String.IsNullOrWhiteSpace(email) || !String.IsNullOrWhiteSpace(password))
                {
                    List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                    req.Add(new KeyValuePair<string, string>("email", email));
                    req.Add(new KeyValuePair<string, string>("password", password));
                    req.Add(new KeyValuePair<string, string>("install_id", installId));


                    Response res = await http_request.MakePostRequest("auth/login", req);
                    JToken data = res.ResponseData;

                    if (res.IsSuccess)
                    {
                        string uuid = (string)data["uuid"];
                        Preferences.Set("uuid", uuid);
                        Application.Current.MainPage = new MainPage();
                    }
                    else
                    {
                        string error_message = data.ToString();
                        if (error_message == "Please confirm your account, an email has been sent to your inbox")
                        {
                            error.Text = error_message;
                            resend_button.IsVisible = true;
                        }
                        else
                        {
                            error.Text = error_message;
                        }
                    }

                }

                else
                {
                    error.Text = "Please fill out valid info in both fields";
                }
            }
            else
            {
                error.Text = "No fcm key set?";
            }
        }

        public async void ResendVerificationEmail(object sender, EventArgs e)
        {
            List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
            req.Add(new KeyValuePair<string, string>("email", loginid.Text));


            Response res = await http_request.MakePostRequest("auth/resend_verification_email", req);
            JToken data = res.ResponseData;

            if (res.IsSuccess)
            {
                error.TextColor = Color.Green;
                error.Text = "Email has been sent, make sure to check your spam folder";
                resend_button.IsVisible = false;
            }


        }

        public ICommand ClickCommand => new Command<string>((url) =>
        {
            Navigation.PushAsync(new RegisterPage());
        });

        public async void RedirectToRegisterPage(object sender, EventArgs e)
        {
            await Navigation.PushAsync(new RegisterPage());
        }
    }
}