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
    public partial class UpdateCurrent : ContentPage
    {
        public string expenseUuid;

        public UpdateCurrent(ExpenseItem selectedExpense)
        {
            InitializeComponent();
            expenseUuid = selectedExpense.Expense_uuid;
        }

        public async void AddCurToDB(Object sender, EventArgs e)
        {
            if (Amount.Text == "0")
            {
                error.Text = "Amount can't be 0.";
            }
            else
            {
                string curAmount = Amount.Text;
                string user_uuid = Preferences.Get("uuid", null);
                if (user_uuid != null)
                {
                    List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                    req.Add(new KeyValuePair<string, string>("expense_uuid", expenseUuid));
                    req.Add(new KeyValuePair<string, string>("uuid", user_uuid));
                    req.Add(new KeyValuePair<string, string>("amount", curAmount));

                    Response res = await http_request.MakePostRequest("user/expenses/update_current", req);
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

        public async void DeleteExpense(Object sender, EventArgs e)
        {
            var response = await DisplayAlert("Delete budget", "Are you sure you want to delete this budget?", "Yes", "No");
            if (response)
            {
                string user_uuid = Preferences.Get("uuid", "null");
                if (user_uuid != "null")
                {
                    List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                    req.Add(new KeyValuePair<string, string>("expense_uuid", expenseUuid));
                    req.Add(new KeyValuePair<string, string>("uuid", user_uuid));

                    Response res = await http_request.MakePostRequest("user/expenses/delete", req);
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
        public async void ClearExpense(Object sender, EventArgs e)
        {
            var response = await DisplayAlert("Clear budget", "Are you sure you want to clear this budget?", "Yes", "No");
            if (response)
            {
                string curAmount = "0";
                string user_uuid = Preferences.Get("uuid", "null");
                if (user_uuid != "null")
                {
                    List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                    req.Add(new KeyValuePair<string, string>("expense_uuid", expenseUuid));
                    req.Add(new KeyValuePair<string, string>("uuid", user_uuid));
                    req.Add(new KeyValuePair<string, string>("amount", curAmount));

                    Response res = await http_request.MakePostRequest("user/expenses/update_current", req);
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