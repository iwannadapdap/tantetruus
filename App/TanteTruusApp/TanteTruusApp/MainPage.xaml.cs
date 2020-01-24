using System;
using System.Collections.Generic;
using Xamarin.Forms;
using Xamarin.Essentials;
using TanteTruusApp.Models;
using TanteTruusApp.Views;
using Newtonsoft.Json.Linq;
using TanteTruusApp.Helpers;

namespace TanteTruusApp
{
    public partial class MainPage : MasterDetailPage
    {
        public List<MasterPageItem> menuList
        {
            get;
            set;
        }
        public MainPage()
        {
            InitializeComponent();
            string key = Preferences.Get("uuid", null);
            menuList = new List<MasterPageItem>();
            // Adding menu items to menuList and you can define title ,page and icon 
            if (key != null)
            {
                menuList.Add(new MasterPageItem()
                {
                    Title = "Account",
                    Icon = "",
                    TargetType = typeof(AccountPage)
                });
            }
            else
            {
                menuList.Add(new MasterPageItem()
                {
                    Title = "Login",
                    Icon = "",
                    TargetType = typeof(LoginPage)
                });
            }
            menuList.Add(new MasterPageItem()
            {
                Title = "Schedule",
                Icon = "",
                TargetType = typeof(SchedulePage)
            });
            menuList.Add(new MasterPageItem()
            {
                Title = "Budget",
                Icon = "",
                TargetType = typeof(BudgetPage)
            });
            menuList.Add(new MasterPageItem()
            {
                Title = "Food",
                Icon = "",
                TargetType = typeof(FoodPage)
            });
            menuList.Add(new MasterPageItem()
            {
                Title = "Hygiene",
                Icon = "",
                TargetType = typeof(HygienePage)
            });
         /*   menuList.Add(new MasterPageItem()
            {
                Title = "Exercise",
                Icon = "",
                TargetType = typeof(ExercisePage)
            }); */
            menuList.Add(new MasterPageItem()
            {
                Title = "Settings",
                Icon = "icon.png",
                TargetType = typeof(SettingsPage)
            });
            menuList.Add(new MasterPageItem()
            {
                Title = "About",
                Icon = "",
                TargetType = typeof(AboutPage)
            });
            // Setting our list to be ItemSource for ListView in MainPage.xaml  
            navigationDrawerList.ItemsSource = menuList;
            // Initial navigation, this can be used for our home page
            if(key != null)
            {
                Detail = new NavigationPage((Page)Activator.CreateInstance(typeof(SchedulePage))) { BarBackgroundColor = Color.FromHex("#222222") };
                IsGestureEnabled = true;
            }
            else
            {
                Detail = new NavigationPage((Page)Activator.CreateInstance(typeof(LoginPage))) { BarBackgroundColor = Color.FromHex("#222222") };
                IsGestureEnabled = false;
            }
        }
        // Event for Menu Item selection, here we are going to handle navigation based  
        // on user selection in menu ListView  
        private void OnMenuItemSelected(object sender, SelectedItemChangedEventArgs e)
        {
            MasterPageItem item = (MasterPageItem)e.SelectedItem;
            Type page = item.TargetType;
            Detail = new NavigationPage((Page)Activator.CreateInstance(page)) {BarBackgroundColor = Color.FromHex("#222222")};
            IsPresented = false;
        }
        protected override async void OnAppearing()
        {
            string user_uuid = Preferences.Get("uuid", null);
            string fcm_key = Preferences.Get("FcmKey", null);
            if (user_uuid != null)
            {
                List<KeyValuePair<string, string>> req = new List<KeyValuePair<string, string>>();
                req.Add(new KeyValuePair<string, string>("uuid", user_uuid));
                req.Add(new KeyValuePair<string, string>("fcm_key", fcm_key));

                Response res = await http_request.MakePostRequest("auth/register_fcm_key", req);
                if (res.IsSuccess)
                {
                    Console.WriteLine("FCM key updated");
                }
            }
        }
    }
}
