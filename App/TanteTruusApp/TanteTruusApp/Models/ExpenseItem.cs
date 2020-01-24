namespace TanteTruusApp.Models
{
    public class ExpenseItem
        {
            public string Title { get; set; }
            public string EstAmount { get; set; }
            public string Type { get; set; }
            public string Expense_uuid { get; set; }
        public string CurAmount { get; set; }

        public ExpenseItem(string _title, string _estAmount, string _type, string _expenseUuid, string _CurAmount)
        {
            Title = _title;
            EstAmount = _estAmount;
            Type = _type;
            Expense_uuid = _expenseUuid;
            CurAmount = _CurAmount;
        }
        }
}