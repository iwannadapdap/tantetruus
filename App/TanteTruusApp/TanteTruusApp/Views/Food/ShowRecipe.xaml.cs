using System;
using TanteTruusApp.Models;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace TanteTruusApp.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class ShowRecipe : ContentPage
    {
        public ShowRecipe(Recipe selectedItem)
        {
            InitializeComponent();
            title_field.Text = selectedItem.Title;
            prepTime_field.Text = "Preparation time: " + selectedItem.PrepTime + " min";

            for(int i = 0; i < selectedItem.Ingredients.Count; i++)
            {
                selectedItem.Ingredients[i] = "- " + selectedItem.Ingredients[i];
            }
            for (int i = 0; i < selectedItem.Preperation.Count; i++)
            {
                selectedItem.Preperation[i] = (i+1).ToString() + ". " + selectedItem.Preperation[i];
            }

            ingredients_field.Text = String.Join(Environment.NewLine, selectedItem.Ingredients);
            preperation_field.Text = String.Join(Environment.NewLine, selectedItem.Preperation);



        }
    }
}