namespace TanteTruusApp.Models
{
    class HygieneItem
    {
        public string Name { get; set; }
        public string Last_time { get; set; }
        public string Frequency { get; set; }
        public bool Task_done { get; set; }

        public HygieneItem(string _name, string _lastTime, string _frequency, bool _taskDone)
        {
            Name = _name;
            Last_time = _lastTime;
            Frequency = _frequency;
            Task_done = _taskDone;
        }
    }
}
