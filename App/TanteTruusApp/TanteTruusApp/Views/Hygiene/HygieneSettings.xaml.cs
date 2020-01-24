using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using TanteTruusApp.Helpers;
using Xamarin.Essentials;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace TanteTruusApp.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class HygieneSettings : ContentPage
    {
        public HygieneSettings()
        {
            InitializeComponent();
        }

        public async void Update_Preferences(Object sender, EventArgs e)
        {
            string sheetsDays = Sheets_reminder.Text;
            string bathroomDays = Bathroom_reminder.Text;
            string houseDays = House_reminder.Text;
            string kitchenDays = Kitchen_reminder.Text;
            string dishesDays = Dishes_reminder.Text;
            string vacuumDays = Vacuum_reminder.Text;
            string user_uuid = Preferences.Get("uuid", null);
            if (string.IsNullOrEmpty(sheetsDays) || string.IsNullOrEmpty(bathroomDays) || string.IsNullOrEmpty(houseDays) || string.IsNullOrEmpty(kitchenDays) || string.IsNullOrEmpty(dishesDays) || string.IsNullOrEmpty(vacuumDays))
            {
                error.Text = "Please enter valid info in each field.";
            }
            else
            {
                if (user_uuid != null)
                {
                    List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                    req.Add(new KeyValuePair<string, string>("uuid", user_uuid));
                    req.Add(new KeyValuePair<string, string>("sheets", sheetsDays));
                    req.Add(new KeyValuePair<string, string>("bathroom", bathroomDays));
                    req.Add(new KeyValuePair<string, string>("house", houseDays));
                    req.Add(new KeyValuePair<string, string>("kitchen", kitchenDays));
                    req.Add(new KeyValuePair<string, string>("dishes", dishesDays));
                    req.Add(new KeyValuePair<string, string>("vacuum", vacuumDays));

                    Response res = await http_request.MakePostRequest("user/hygiene/update_reminders", req);
                    JToken data = res.ResponseData;

                    if (res.IsSuccess)
                    {
                        await Navigation.PopAsync();
                    }
                    else
                    {
                        error.Text = res.ResponseData.Value<string>();
                    }
                }
                else
                {
                    throw new ArgumentException("Uuid is not set");
                }
            }
        }
    }
}