using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using TanteTruusApp.Helpers;
using Xamarin.Essentials;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace TanteTruusApp.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class AddEvent : ContentPage
    {
        public AddEvent(DateTime? input_date = null)
        {
            InitializeComponent();
            notification_picker.SelectedIndex = 0;

            DateTime date;
            if (input_date == null)
            {
                date = DateTime.Now;
            }
            else
            {
                date = (DateTime)input_date;
            }
            string hour = DateTime.Now.ToString("HH");
            string minutes = DateTime.Now.ToString("mm");
            string seconds = "00";
            TimeSpan time = new TimeSpan(Convert.ToInt32(hour), Convert.ToInt32(minutes), Convert.ToInt32(seconds));


            startdate_field.Date = date;
            enddate_field.Date = date;
            starttime_field.Time = time;
            endtime_field.Time = time;
        }

        private void SyncStartAndEnd(object sender, EventArgs e)
        {
            endtime_field.Time = starttime_field.Time.Add(TimeSpan.FromMinutes(30));
            enddate_field.Date = startdate_field.Date;
        }


        public async void AddEventToDB(Object sender, EventArgs e)
        {
            string title = title_field.Text;
            string notificationTime;
            int notificationTimeInt;
            string content = content_field.Text;
            string location = location_field.Text;
            string startdate = startdate_field.Date.ToString("dd/MM/yyyy");
            string enddate = enddate_field.Date.ToString("dd/MM/yyyy");
            string starttime = starttime_field.Time.ToString(@"hh\:mm\:ss");
            string endtime = endtime_field.Time.ToString(@"hh\:mm\:ss");
            string start = startdate + " " + starttime;
            string end = enddate + " " + endtime;


            try
            {
                notificationTimeInt = int.Parse(notification_field.Text);
            }
            catch
            {
                throw new ArgumentException("Notification time must be an integer");
            }
            if (notification_picker.SelectedIndex == 1)
            {
                notificationTimeInt = notificationTimeInt * 60;
            }
            if (notification_picker.SelectedIndex == 2)
            {
                notificationTimeInt = notificationTimeInt * 60 * 24;
            }
            notificationTime = notificationTimeInt.ToString();
            string user_uuid = Preferences.Get("uuid", null);
            if (user_uuid != null)
            {
                List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                req.Add(new KeyValuePair<string, string>("uuid", user_uuid));
                req.Add(new KeyValuePair<string, string>("title", title));
                req.Add(new KeyValuePair<string, string>("content", content));
                req.Add(new KeyValuePair<string, string>("location", location));
                req.Add(new KeyValuePair<string, string>("start", start));
                req.Add(new KeyValuePair<string, string>("end", end));
                req.Add(new KeyValuePair<string, string>("remind_minutes_before", notificationTime));

                Response res = await http_request.MakePostRequest("user/schedule/update", req);
                JToken data = res.ResponseData;

                if (res.IsSuccess)
                {
                    await Navigation.PopAsync();
                }
                else
                {
                    error.Text = data.ToString();
                }
            }
            else
            {
                throw new ArgumentException("Uuid is not set");
            }
        }
    }


}