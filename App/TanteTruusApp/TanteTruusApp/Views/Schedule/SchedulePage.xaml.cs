using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Globalization;
using System.Linq;
using System.Threading.Tasks;
using Xamarin.Essentials;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;
using XamForms.Controls;
using TanteTruusApp.Models;
using TanteTruusApp.Helpers;

namespace TanteTruusApp.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class SchedulePage : ContentPage
    {
        public SchedulePage()
        {
            InitializeComponent();
        }

        protected override async void OnAppearing()
        {
            CultureInfo MyCultureInfo = new CultureInfo("fr-FR");

            List<ScheduleItem> schedule = await getUserSchedule();
            if (schedule == null)
            {
                return;
            }            

            AddSpecialDateWithList(schedule);
            DayPageStack.IsVisible = false;
            calendar.SelectedDate = null;
        }

        public async void dateClicked(Object sender, EventArgs e)
        {
            XamForms.Controls.Calendar calender = sender as XamForms.Controls.Calendar;
            DateTime selectedDate = (DateTime)calender.SelectedDate;
            if (selectedDate < DateTime.Today)
            {
                AddEventToDayButton.IsVisible = false;
            }
            else
            {
                AddEventToDayButton.IsVisible = true;
            }
            string stringDate = selectedDate.ToString("dd/MM/yyyy");
            DateHeader.Text = stringDate;
            scheduleListXAML.ItemsSource = await getUserScheduleByDate(stringDate);
            DayPageStack.IsVisible = true;
        }

        private void CloseDayButton_Clicked(object sender, EventArgs e)
        {
            DayPageStack.IsVisible = false;
        }

        private async void AddEventToDayButton_Clicked(object sender, EventArgs e)
        {
            await Navigation.PushAsync(new AddEvent((DateTime)calendar.SelectedDate));
        }

        async void OnScheduleItemSelected(Object sender, SelectedItemChangedEventArgs e)
        {
            if (scheduleListXAML.SelectedItem != null)
            {
                ScheduleItem selectedItem = (ScheduleItem)e.SelectedItem;
                string messageUuid = selectedItem.EventUuid;
                string messageTitle = selectedItem.Title;
                string messageNotificationTime = selectedItem.NotificationTime;
                string messageContent = selectedItem.Content;
                string messageLocation = selectedItem.Location;
                string messageStartDate = selectedItem.Start.ToString("dd MMMMM");
                string messageStartTime = selectedItem.Start.ToString("HH:mmu");
                string messageEndDate = selectedItem.End.ToString("dd MMMM");
                string messageEndTime = selectedItem.End.ToString("HH:mmu");
                bool answer;

                if (messageStartDate == messageEndDate)
                {
                    answer = await DisplayAlert(messageTitle + " at " + messageStartDate,
                                                        "From " + messageStartTime +
                                                        " until " + messageEndTime + "." +
                                                        Environment.NewLine + Environment.NewLine + "Location: " + messageLocation +
                                                        Environment.NewLine + Environment.NewLine + "Content: " + messageContent,
                                                        "Edit", "Close");
                }
                else
                {
                    answer = await DisplayAlert(messageTitle,
                                                        "Starts: " + messageStartDate + " at " + messageStartTime + "." + Environment.NewLine +
                                                        "Ends: " + messageEndDate + " at " + messageEndTime + "." +
                                                        Environment.NewLine + Environment.NewLine + "Location: " + messageLocation +
                                                        Environment.NewLine + Environment.NewLine + "Content: " + messageContent,
                                                        "Edit", "Close");
                }
                scheduleListXAML.SelectedItem = null;
                if (answer)
                {
                    await Navigation.PushAsync(new EditEvent(selectedItem));
                }
            }
        }

        private async Task<List<ScheduleItem>> getUserSchedule()
        {
            // Start/end: 6/15/2009 13:45
            string user_uuid = Preferences.Get("uuid", null);
            if (user_uuid != null)
            {
                List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                req.Add(new KeyValuePair<string, string>("uuid", user_uuid));

                Response res = await http_request.MakePostRequest("user/schedule/get", req);
                if (res.IsSuccess)
                {
                    List<ScheduleItem> schedule = new List<ScheduleItem>();
                    JObject data = JObject.Parse(res.ResponseData.ToString());
                    object[] events = data["schedule"].ToObject<object[]>();
                    foreach (object c_event in events)
                    {
                        JObject json_event = JObject.Parse(c_event.ToString());
                        string eventUuid = json_event["event_uuid"].Value<string>();
                        string start = json_event["start"].Value<string>();
                        string end = json_event["end"].Value<string>();
                        string title = json_event["title"].Value<string>();
                        string notificationTime = json_event["remind_minutes_before"].Value<string>();
                        string content = json_event["content"].Value<string>();
                        string location = json_event["location"].Value<string>();

                        ScheduleItem new_item = new ScheduleItem(eventUuid, start, end, title, notificationTime, content, location);
                        schedule.Add(new_item);
                    }
                    Console.WriteLine("============================== data ===================================");
                    Console.WriteLine(schedule);
                    schedule = schedule.OrderBy(x => x.Start).ToList();
                    return schedule;
                }
                return null;

            }
            else
            {
                throw new ArgumentException("Uuid is not set");
            }
        }

        private async Task<List<ScheduleItem>> getUserScheduleByDate(string date)
        {
            // Start/end: 6/15/2009 13:45
            string user_uuid = Preferences.Get("uuid", null);
            if (user_uuid != null)
            {
                List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                req.Add(new KeyValuePair<string, string>("uuid", user_uuid));
                req.Add(new KeyValuePair<string, string>("date", date));

                Response res = await http_request.MakePostRequest("user/schedule/get_date", req);
                if (res.IsSuccess)
                {
                    List<ScheduleItem> schedule = new List<ScheduleItem>();
                    JObject data = JObject.Parse(res.ResponseData.ToString());
                    object[] events = data["schedule"].ToObject<object[]>();
                    foreach (object c_event in events)
                    {
                        JObject json_event = JObject.Parse(c_event.ToString());
                        string eventUuid = json_event["event_uuid"].Value<string>();
                        string start = json_event["start"].Value<string>();
                        string end = json_event["end"].Value<string>();
                        string title = json_event["title"].Value<string>();
                        string notification_time = json_event["remind_minutes_before"].Value<string>();
                        string content = json_event["content"].Value<string>();
                        string location = json_event["location"].Value<string>();

                        ScheduleItem new_item = new ScheduleItem(eventUuid, start, end, title, notification_time, content, location);
                        schedule.Add(new_item);
                    }
                    Console.WriteLine("============================== data ===================================");
                    Console.WriteLine(schedule);
                    schedule = schedule.OrderBy(x => x.Start).ToList();
                    return schedule;
                }
                return null;

            }
            else
            {
                throw new ArgumentException("Uuid is not set");
            }
        }

        public async void Add_Clicked(Object sender, EventArgs e)
        {
            await Navigation.PushAsync(new AddEvent());
        }
        /* Code for xamforms calendar package*/
        private DateTime? _date;
        public DateTime? Date
        {
            get
            {
                return _date;
            }
            set
            {
                _date = value;
                OnPropertyChanged(nameof(Date));
            }
        }

        private ObservableCollection<XamForms.Controls.SpecialDate> attendances;
        public ObservableCollection<XamForms.Controls.SpecialDate> Attendances
        {
            get
            {
                return attendances;
            }
            set
            {
                attendances = value;
                OnPropertyChanged(nameof(Attendances));
            }
        }

        public void AddSpecialDateWithList(List<ScheduleItem> list)
        {
            List<SpecialDate> newList = new List<SpecialDate>();
            foreach (ScheduleItem model in list)
            {
                SpecialDate newDate = new SpecialDate(model.Start)
                {
                    Selectable = true,
                    BackgroundPattern = new BackgroundPattern(1)
                    {
                        Pattern = new List<Pattern>
                         {
                             new Pattern { WidthPercent = 1f, HightPercent = 1f, Color = Color.Red }
                         }
                    },
                };

                newList.Add(newDate);
            }
            calendar.SpecialDates = newList;
        }

        /* End code for xamforms calendar package*/
    }

}