using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using TanteTruusApp.Models;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;
using Newtonsoft.Json.Linq;
using TanteTruusApp.Helpers;

namespace TanteTruusApp.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class FoodPage : ContentPage
    {
        public FoodPage()
        {
            InitializeComponent();
        }

        protected async override void OnAppearing()
        {
            recipeListXAML.ItemsSource = await GetRecipesFromDatabase();
        }

        private async Task<List<Recipe>> GetRecipesFromDatabase()
        {
            Response res = await http_request.MakeGetRequest("/food/get");
            if (res.IsSuccess)
            {
                List<Recipe> r_recipes = new List<Recipe>();
                JObject data = JObject.Parse(res.ResponseData.ToString());
                object[] recipes = data["recipes"].ToObject<object[]>();
                foreach (object c_recipe in recipes)
                {
                    JObject json_event = JObject.Parse(c_recipe.ToString());
                    string uuid = json_event["recipe_uuid"].Value<string>();
                    string title = json_event["title"].Value<string>();
                    string prep_time = json_event["prep_time"].Value<string>();
                    List<string> ingredients = json_event["ingredients"].ToObject<List<string>>();
                    List<string> preperation = json_event["preperation"].ToObject<List<string>>();

                    Recipe new_item = new Recipe(uuid, title, prep_time, ingredients, preperation);
                    r_recipes.Add(new_item);
                }
                Console.WriteLine("============================== data ===================================");
                Console.WriteLine(recipes);
                return r_recipes;
            }
            return null;
        }

        public async void OnRecipeSelected(Object sender, SelectedItemChangedEventArgs e)
        {
            var detailPage = new ShowRecipe(e.SelectedItem as Recipe);
            await Navigation.PushAsync(detailPage);
        }
    }
}