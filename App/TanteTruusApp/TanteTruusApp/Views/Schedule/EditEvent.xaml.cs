using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using Xamarin.Essentials;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;
using TanteTruusApp.Models;
using TanteTruusApp.Helpers;

namespace TanteTruusApp.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class EditEvent : ContentPage
    {
        private string event_uuid;
        public EditEvent(ScheduleItem selecteditem)
        {
            InitializeComponent();
            notification_picker.SelectedIndex = 0;
            event_uuid = selecteditem.EventUuid;
            string title = selecteditem.Title;
            string notificationTime = selecteditem.NotificationTime;
            string content = selecteditem.Content;
            string location = selecteditem.Location;
            DateTime startDate = selecteditem.Start;
            TimeSpan startTime = selecteditem.Start.TimeOfDay;
            DateTime endDate = selecteditem.End;
            TimeSpan endTime = selecteditem.End.TimeOfDay;

            title_field.Text = title;
            notification_field.Text = notificationTime;
            content_field.Text = content;
            location_field.Text = location;
            startdate_field.Date = startDate;
            starttime_field.Time = startTime;
            enddate_field.Date = endDate;
            endtime_field.Time = endTime;
        }

        private void SyncStartAndEnd(object sender, EventArgs e)
        {
            endtime_field.Time = starttime_field.Time.Add(TimeSpan.FromMinutes(30));
            enddate_field.Date = startdate_field.Date;
        }

        public async void EditEventToDB(Object sender, EventArgs e)
        {
            int notificationTimeInt;
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
            string title = title_field.Text;
            string notificationTime = notificationTimeInt.ToString();
            string content = content_field.Text;
            string location = location_field.Text;
            string startdate = startdate_field.Date.ToString("dd/MM/yyyy");
            string enddate = enddate_field.Date.ToString("dd/MM/yyyy");
            string starttime = starttime_field.Time.ToString();
            string endtime = endtime_field.Time.ToString();
            string start = startdate + " " + starttime;
            string end = enddate + " " + endtime;

            string user_uuid = Preferences.Get("uuid", null);
            if (user_uuid != null)
            {
                List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                req.Add(new KeyValuePair<string, string>("event_uuid", event_uuid));
                req.Add(new KeyValuePair<string, string>("uuid", user_uuid));
                req.Add(new KeyValuePair<string, string>("title", title));
                req.Add(new KeyValuePair<string, string>("remind_minutes_before", notificationTime));
                req.Add(new KeyValuePair<string, string>("content", content));
                req.Add(new KeyValuePair<string, string>("location", location));
                req.Add(new KeyValuePair<string, string>("start", start));
                req.Add(new KeyValuePair<string, string>("end", end));

                Response res = await http_request.MakePostRequest("user/schedule/update", req);
                JToken data = res.ResponseData;

                if (res.IsSuccess)
                {
                    await Navigation.PushAsync(new SchedulePage());
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
        private async void DeleteEvent(Object sender, EventArgs e)
        {
            var response = await DisplayAlert("Delete Event", "Are you sure you want to delete this event?", "Yes", "No");
            if (response)
            {
                string user_uuid = Preferences.Get("uuid", null);
                if (user_uuid != null)
                {
                    List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                    req.Add(new KeyValuePair<string, string>("event_uuid", event_uuid));
                    req.Add(new KeyValuePair<string, string>("uuid", user_uuid));

                    Response res = await http_request.MakePostRequest("user/schedule/delete", req);
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
