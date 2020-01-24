using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Threading.Tasks;
using TanteTruusApp.Models;
using TanteTruusApp.Helpers;
using Xamarin.Essentials;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace TanteTruusApp.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class BudgetPage : ContentPage
    {
        public List<ExpenseItem> expenseList
        {
            get;
            set;
        }
        public BudgetPage()
        {
            InitializeComponent();
        }
        private async void OnExpensesItemSelected(object sender, SelectedItemChangedEventArgs e)
        {
            ExpenseItem selectedExpense = (ExpenseItem)e.SelectedItem;
            await Navigation.PushAsync(new UpdateCurrent(selectedExpense));
        }
        protected override async void OnAppearing()
        {
            CultureInfo MyCultureInfo = new CultureInfo("fr-FR");

            List<ExpenseItem> expense = await getUserExpenses();
            if (expense == null)
            {
                return;
            }
            ExpensesListXAML.ItemsSource = expense;
        }

        private async Task<List<ExpenseItem>> getUserExpenses()
        {
            // Start/end: 6/15/2009 13:45
            string user_uuid = Preferences.Get("uuid", null);
            if (user_uuid != null)
            {
                List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>
                {
                    new KeyValuePair<string, string>("uuid", user_uuid)
                };

                Response res = await http_request.MakePostRequest("user/expenses/get", req);
                if (res.IsSuccess)
                {
                    List<ExpenseItem> expense = new List<ExpenseItem>();
                    JObject data = JObject.Parse(res.ResponseData.ToString());
                    object[] events = data["expenses"].ToObject<object[]>();
                    foreach (object c_event in events)
                    {
                        JObject json_event = JObject.Parse(c_event.ToString());
                        string expenseuuid = json_event["expense_uuid"].Value<string>();
                        string title = json_event["title"].Value<string>();
                        string curamount = json_event["cur_amount"].Value<string>();
                        string estamount = json_event["est_amount"].Value<string>();
                        string type = json_event["expense_type"].Value<string>();
                        ExpenseItem new_item = new ExpenseItem(title, estamount, type, expenseuuid, curamount);
                        expense.Add(new_item);
                    }
                    object[] events2 = data["incomes"].ToObject<object[]>();
                    foreach (object c_event2 in events2)
                    {
                        JObject json_event = JObject.Parse(c_event2.ToString());
                        string expenseuuid = json_event["expense_uuid"].Value<string>();
                        string title = json_event["title"].Value<string>();
                        string curamount = json_event["cur_amount"].Value<string>();
                        string estamount = json_event["est_amount"].Value<string>();
                        string type = json_event["expense_type"].Value<string>();
                        ExpenseItem new_item = new ExpenseItem(title, estamount, type, expenseuuid, curamount);
                        expense.Add(new_item);
                    }
                    string curBalance = data["cur_balance"].ToString();
                    cur_balanceLabel.Text = curBalance;
                    string estBalance = data["est_balance"].ToString();
                    est_balanceLabel.Text = estBalance;
                    Console.WriteLine("============================== data ===================================");
                    Console.WriteLine(expense);
                    expense = expense.OrderBy(x => x.Type).ToList();
                    return expense;
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
            await Navigation.PushAsync(new AddBudget());
        }
    }
}