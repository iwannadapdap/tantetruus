using Android.App;
using Android.Content.PM;
using Android.Gms.Extensions;
using Android.OS;
using Android.Runtime;
using Firebase.Iid;
using Firebase.Messaging;
using TanteTruusApp.Helpers;
using System.Collections.Generic;
using Xamarin.Essentials;
using Newtonsoft.Json.Linq;

namespace TanteTruusApp.Droid
{
    [Activity(Label = "TanteTruusApp", Icon = "@mipmap/icon", Theme = "@style/MainTheme", MainLauncher = true, ConfigurationChanges = ConfigChanges.ScreenSize | ConfigChanges.Orientation)]
    public class MainActivity : global::Xamarin.Forms.Platform.Android.FormsAppCompatActivity
    {
        protected async override void OnCreate(Bundle savedInstanceState)
        {
            TabLayoutResource = Resource.Layout.Tabbar;
            ToolbarResource = Resource.Layout.Toolbar;

            base.OnCreate(savedInstanceState);
            IInstanceIdResult result = await FirebaseInstanceId.Instance.GetInstanceId().AsAsync<IInstanceIdResult>();
            string token = result.Token;
            string FcmKey = token.ToString();
            Preferences.Set("FcmKey", FcmKey);

            Xamarin.Essentials.Platform.Init(this, savedInstanceState);
            global::Xamarin.Forms.Forms.Init(this, savedInstanceState);

            ZXing.Mobile.MobileBarcodeScanner.Initialize(this.Application);
            LoadApplication(new App());
        }

        public override void OnRequestPermissionsResult(int requestCode, string[] permissions, [GeneratedEnum] Android.Content.PM.Permission[] grantResults)
        {
            Xamarin.Essentials.Platform.OnRequestPermissionsResult(requestCode, permissions, grantResults);
            global::ZXing.Net.Mobile.Android.PermissionsHandler.OnRequestPermissionsResult(requestCode, permissions, grantResults);
            base.OnRequestPermissionsResult(requestCode, permissions, grantResults);
        }
    }

    
}

