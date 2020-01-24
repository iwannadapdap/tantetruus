using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using TanteTruusApp.Helpers;
using TanteTruusApp.Models;
using Xamarin.Essentials;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace TanteTruusApp.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class HygienePage : ContentPage
    {
        public HygienePage()
        {
            InitializeComponent();
        }
        protected override async void OnAppearing()
        {
            CultureInfo MyCultureInfo = new CultureInfo("fr-FR");

            List<HygieneItem> hygiene = await getHygiene();
            if (hygiene == null)
            {
                return;
            }
            SheetsLabel.Text = hygiene[0].Name;
            BathroomLabel.Text = hygiene[1].Name;
            HouseLabel.Text = hygiene[2].Name;
            KitchenLabel.Text = hygiene[3].Name;
            DishesLabel.Text = hygiene[4].Name;
            VacuumLabel.Text = hygiene[5].Name;

            SheetsDateLabel.Text = "Prev: " + hygiene[0].Last_time;
            BathroomDateLabel.Text = "Prev: " + hygiene[1].Last_time;
            HouseDateLabel.Text = "Prev: " + hygiene[2].Last_time;
            KitchenDateLabel.Text = "Prev: " + hygiene[3].Last_time;
            DishesDateLabel.Text = "Prev: " + hygiene[4].Last_time;
            VacuumDateLabel.Text = "Prev: " + hygiene[5].Last_time;

            if (hygiene[0].Task_done)
            {
                SheetsXLabel.Text = " ✔";
                SheetsXLabel.TextColor = Color.Green;
            }
            else
            {
                SheetsXLabel.Text = " ✘";
                SheetsXLabel.TextColor = Color.Red;
            }
            if (hygiene[1].Task_done)
            {
                BathroomXLabel.Text = " ✔";
                BathroomXLabel.TextColor = Color.Green;
            }
            else
            {
                BathroomXLabel.Text = " ✘";
                BathroomXLabel.TextColor = Color.Red;
            }
            if (hygiene[2].Task_done)
            {
                HouseXLabel.Text = " ✔";
                HouseXLabel.TextColor = Color.Green;
            }
            else
            {
                HouseXLabel.Text = " ✘";
                HouseXLabel.TextColor = Color.Red;
            }
            if (hygiene[3].Task_done)
            {
                KitchenXLabel.Text = " ✔";
                KitchenXLabel.TextColor = Color.Green;
            }
            else
            {
                KitchenXLabel.Text = " ✘";
                KitchenXLabel.TextColor = Color.Red;
            }
            if (hygiene[4].Task_done)
            {
                DishesXLabel.Text = " ✔";
                DishesXLabel.TextColor = Color.Green;
            }
            else
            {
                DishesXLabel.Text = " ✘";
                DishesXLabel.TextColor = Color.Red;
            }
            if (hygiene[5].Task_done)
            {
                VacuumXLabel.Text = " ✔";
                VacuumXLabel.TextColor = Color.Green;
            }
            else
            {
                VacuumXLabel.Text = " ✘";
                VacuumXLabel.TextColor = Color.Red;
            }
        }

        private async void Open_Settings(Object sender, EventArgs e)
        {
            await Navigation.PushAsync(new HygieneSettings());
        }

        private async void Open_Help(Object sender, EventArgs e)
        {
            await Navigation.PushAsync(new HygieneHelp());
        }

        private async Task<List<HygieneItem>> getHygiene()
        {
            // Start/end: 6/15/2009 13:45
            string user_uuid = Preferences.Get("uuid", null);
            if (user_uuid != null)
            {
                List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                req.Add(new KeyValuePair<string, string>("uuid", user_uuid));

                Response res = await http_request.MakePostRequest("user/hygiene/get", req);
                if (res.IsSuccess)
                {
                    List<HygieneItem> hygiene = new List<HygieneItem>();
                    JObject data = JObject.Parse(res.ResponseData.ToString());
                    object[] events = data["hygiene"]["hygiene"].ToObject<object[]>();
                    foreach (object c_event in events)
                    {
                        JObject json_event = JObject.Parse(c_event.ToString());
                        string name = json_event["name"].Value<string>();
                        string lastTime = json_event["last_time"].Value<string>();
                        string frequency = json_event["frequency"].Value<string>();
                        bool taskDone = json_event["task_done"].Value<bool>();

                        HygieneItem new_item = new HygieneItem(name, lastTime, frequency, taskDone);
                        hygiene.Add(new_item);
                    }
                    Console.WriteLine("============================== data ===================================");
                    return hygiene;
                }
                return null;

            }
            else
            {
                throw new ArgumentException("Uuid is not set");
            }
        }

        public async void UpdateHygiene(string name, string done)
        {
            string hygieneName = name;
            string taskDone = done;
            string user_uuid = Preferences.Get("uuid", null);
            if (user_uuid != null)
            {
                List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                req.Add(new KeyValuePair<string, string>("hygiene_name", hygieneName));
                req.Add(new KeyValuePair<string, string>("uuid", user_uuid));
                req.Add(new KeyValuePair<string, string>("is_done", done));

                Response res = await http_request.MakePostRequest("user/hygiene/update", req);
                JToken data = res.ResponseData;

                if (res.IsSuccess)
                {
                    OnAppearing();
                }
                else
                {
                    await DisplayAlert("Error", res.ResponseData.Value<string>(), "Ok");
                }
            }
            else
            {
                throw new ArgumentException("Uuid is not set");
            }
        }
        public async void SheetsDone(Object sender, EventArgs e)
        {
            if (SheetsXLabel.TextColor == Color.Red)
            {
                bool answer = await DisplayAlert("Confirm", "Did you wash your sheets?", "Yes", "No");
                if (answer)
                {
                    UpdateHygiene(SheetsLabel.Text, "true");
                }
            }
            else
            {
                bool answer = await DisplayAlert("Confirm", "Do you want to set this task to undone?", "Yes", "No");
                if(answer)
                {
                    UpdateHygiene(SheetsLabel.Text, "false");
                }
            }
        }

        public async void BathroomDone(Object sender, EventArgs e)
        {
            if (BathroomXLabel.TextColor == Color.Red)
            {
                bool answer = await DisplayAlert("Confirm", "Did you clean the bathroom?", "Yes", "No");
                if (answer)
                {
                    UpdateHygiene(BathroomLabel.Text, "true");
                }
            }
            else
            {
                bool answer = await DisplayAlert("Confirm", "Do you want to set this task to undone?", "Yes", "No");
                if (answer)
                {
                    UpdateHygiene(BathroomLabel.Text, "false");
                }
            }
        }

        public async void HouseDone(Object sender, EventArgs e)
        {
            if (HouseXLabel.TextColor == Color.Red)
            {
                bool answer = await DisplayAlert("Confirm", "Did you clean the house?", "Yes", "No");
                if (answer)
                {
                    UpdateHygiene(HouseLabel.Text, "true");
                }
            }
            else
            {
                bool answer = await DisplayAlert("Confirm", "Do you want to set this task to undone?", "Yes", "No");
                if (answer)
                {
                    UpdateHygiene(HouseLabel.Text, "false");
                }
            }
        }

        public async void KitchenDone(Object sender, EventArgs e)
        {
            if (KitchenXLabel.TextColor == Color.Red)
            {
                bool answer = await DisplayAlert("Confirm", "Did you clean the kitchen?", "Yes", "No");
                if (answer)
                {
                    UpdateHygiene(KitchenLabel.Text, "true");
                }
            }
            else
            {
                bool answer = await DisplayAlert("Confirm", "Do you want to set this task to undone?", "Yes", "No");
                if (answer)
                {
                    UpdateHygiene(KitchenLabel.Text, "false");
                }
            }
        }

        public async void VacuumDone(Object sender, EventArgs e)
        {
            if (VacuumXLabel.TextColor == Color.Red)
            {
                bool answer = await DisplayAlert("Confirm", "Did you vacuum the house?", "Yes", "No");
                if (answer)
                {
                    UpdateHygiene(VacuumLabel.Text, "true");
                }
            }
            else
            {
                bool answer = await DisplayAlert("Confirm", "Do you want to set this task to undone?", "Yes", "No");
                if (answer)
                {
                    UpdateHygiene(VacuumLabel.Text, "false");
                }
            }
        }

        public async void DishesDone(Object sender, EventArgs e)
        {
            if (DishesXLabel.TextColor == Color.Red)
            {
                bool answer = await DisplayAlert("Confirm", "Did you do the dishes?", "Yes", "No");
                if (answer)
                {
                    UpdateHygiene(DishesLabel.Text, "true");
                }
            }
            else
            {
                bool answer = await DisplayAlert("Confirm", "Do you want to set this task to undone?", "Yes", "No");
                if (answer)
                {
                    UpdateHygiene(DishesLabel.Text, "false");
                }
            }
        }
    }
}