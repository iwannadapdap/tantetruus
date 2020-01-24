using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Xamarin.Essentials;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;
using TanteTruusApp.Helpers;
using TanteTruusApp.Models;

namespace TanteTruusApp.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class SettingsPage : ContentPage
    {
        public SettingsPage()
        {
            InitializeComponent();
        }

        protected override async void OnAppearing()
        {
            var preferences = await GetUserPreferences();

            notifications_enabled_switch.IsToggled = preferences.notificationsEnabled;
            alarm_enabled_switch.IsToggled = preferences.alarmEnabled;
        }

        private class UserPreferences
        {
            public bool notificationsEnabled { get; set; }
            public bool alarmEnabled { get; set; }

            public UserPreferences(bool notifications_enabled, bool alarm_enabled)
            {
                notificationsEnabled = notifications_enabled;
                alarmEnabled = alarm_enabled;
            }
        }

        private async void UpdatePreferences_Clicked(object sender, EventArgs e)
        {
            bool notifications_enabled = notifications_enabled_switch.IsToggled;
            bool alarm_enabled = alarm_enabled_switch.IsToggled;

            bool updated = await UpdateUserPreferences(notifications_enabled, alarm_enabled);

            if (updated)
            {
                message_label.TextColor = Color.Green;
                message_label.Text = "Preferences updated successfully";
            }
            else
            {
                message_label.TextColor = Color.Red;
                message_label.Text = "Preferences not updated";
            }
        }

        private async Task<UserPreferences> GetUserPreferences()
        {
            string user_uuid = Preferences.Get("uuid", null);
            if (user_uuid != null)
            {
                List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                req.Add(new KeyValuePair<string, string>("uuid", user_uuid));

                Response res = await http_request.MakePostRequest("user/preferences/get", req);
                if (res.IsSuccess)
                {
                    JObject data = JObject.Parse(res.ResponseData.ToString());

                    bool notifications_enabled = data["preferences"]["notifications_enabled"].Value<bool>();
                    bool alarm_enabled = data["preferences"]["alarm_enabled"].Value<bool>();

                    UserPreferences preferences = new UserPreferences(notifications_enabled, alarm_enabled);

                    return preferences;
                }
                return null;
            }
            else
            {
                throw new ArgumentException("UUID is not set");
            }
        }

        private async Task<bool> UpdateUserPreferences(bool notifications_enabled, bool alarm_enabled)
        {
            string user_uuid = Preferences.Get("uuid", null);
            if (user_uuid != null)
            {
                List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                req.Add(new KeyValuePair<string, string>("uuid", user_uuid));
                req.Add(new KeyValuePair<string, string>("notifications_enabled", notifications_enabled.ToString()));
                req.Add(new KeyValuePair<string, string>("alarm_enabled", alarm_enabled.ToString()));
                Response res = await http_request.MakePostRequest("user/preferences/update", req);
                if (res.IsSuccess)
                {
                    return true;
                }
                return false;
            }
            else
            {
                throw new ArgumentException("UUID is not set");
            }
        }
        public async void Add_Arduino(Object sender, EventArgs e)
        {
            try
            {
                var scanner = DependencyService.Get<IQrScanningService>();
                string result = await scanner.ScanAsync();
                if (result != null)
                {
                    string arduino_uuid = result;
                    string user_uuid = Preferences.Get("uuid", null);

                    if (user_uuid != null)
                    {
                        User new_user = new User();
                        List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                        req.Add(new KeyValuePair<string, string>("uuid", user_uuid));
                        req.Add(new KeyValuePair<string, string>("arduino_uuid", arduino_uuid));

                        Response res = await http_request.MakePostRequest("user/link_arduino", req);
                        if (!res.IsSuccess)
                        {
                            error.Text = res.Message;
                        }
                    }


                }
            }
            catch (Exception ex)
            {
                throw ex;
            }

        }
    }
}