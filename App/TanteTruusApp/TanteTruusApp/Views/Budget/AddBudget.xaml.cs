using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using TanteTruusApp.Helpers;
using Xamarin.Essentials;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace TanteTruusApp.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class AddBudget : ContentPage
    {
        public AddBudget()
        {
            InitializeComponent();
        }

        public async void AddBudgetToDB(Object sender, EventArgs e)
        {
            string title = title_field.Text;
            string type = picker_field.SelectedItem.ToString();
            if (type == "Expense") type = "exp";
            if (type == "Income") type = "inc";
            string est_amount = estamount_field.Text;

            string user_uuid = Preferences.Get("uuid", null);
            if (user_uuid != null)
            {
                List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>
                {
                    new KeyValuePair<string, string>("uuid", user_uuid),
                    new KeyValuePair<string, string>("title", title),
                    new KeyValuePair<string, string>("est_amount", est_amount),
                    new KeyValuePair<string, string>("expense_type", type),
                };

                Response res = await http_request.MakePostRequest("user/expenses/update", req);
                 JToken data = res.ResponseData;

                 if (res.IsSuccess)
                 {
                     await Navigation.PopAsync();
                 }
                 else
                 {
                     error.Text = res.ResponseData.Value<string>();
                 }
                error.Text = user_uuid;
            }
            else
            {
                throw new ArgumentException("Uuid is not set");
            }
        }
    }
}