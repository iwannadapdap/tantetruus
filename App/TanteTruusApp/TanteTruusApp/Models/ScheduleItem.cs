using System;
using System.Globalization;

namespace TanteTruusApp.Models
{

    public class ScheduleItem
    {
        public ScheduleItem(string _eventuuid, string _start, string _end, string _title, string _notificationTime, string _content = null, string _location = null)
        {
            try
            {
                Start = DateTime.ParseExact(_start, "dd/MM/yyyy HH:mm:ss", CultureInfo.InvariantCulture);
                End = DateTime.ParseExact(_end, "dd/MM/yyyy HH:mm:ss", CultureInfo.InvariantCulture);
            }
            catch (Exception e)
            {
                throw new Exception(e.ToString());
            }
            EventUuid = _eventuuid;
            Title = _title;
            NotificationTime = _notificationTime;
            Content = _content;
            Location = _location;
        }

        public string EventUuid { get; set; }
        public DateTime Start { get; set; }
        public DateTime End { get; set; }
        public string Title { get; set; }
        public string NotificationTime { get; set; }
        public string Content { get; set; }
        public string Location { get; set; }
    }
}
