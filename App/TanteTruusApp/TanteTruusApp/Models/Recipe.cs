using System.Collections.Generic;

namespace TanteTruusApp.Models
{
    public class Recipe
    {
        string Uuid { get; set; }
        public string Title { get; set; }
        public string PrepTime { get; set; }
        public List<string>  Ingredients { get; set; }
        public List<string> Preperation { get; set; }

        public Recipe(string _uuid, string _title, string _cookTime, List<string> _ingredients, List<string> _preperation)
        {
            Uuid = _uuid;
            Title = _title;
            PrepTime = _cookTime;
            Ingredients = _ingredients;
            Preperation = _preperation;
        }
    }
}
