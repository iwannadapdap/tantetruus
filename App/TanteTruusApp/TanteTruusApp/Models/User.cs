using System;
using System.Globalization;

namespace TanteTruusApp.Models
{
        class User
        {
            public string Name { get; set; }
            public string Email { get; set; }
            public string Created_at { get; set; }
            public string Last_login { get; set; }
            public DateTime Birthdate { get; set; }
            public int Age
            {
                get
                {
                    int years =  DateTime.Today.Year - Birthdate.Year;

                    if (Birthdate < DateTime.Today)
                    {
                        years -= 1;
                    }
                    return years;
                }
            }

            public User(string name, string email, string birthdate, string created_at, string last_login)
            {
                Name = name;
                Email = email;
                Created_at = created_at.Remove(created_at.Length - 7);
                Last_login = last_login;
                try
                {
                    Birthdate = DateTime.ParseExact(birthdate, "dd/MM/yyyy", CultureInfo.InvariantCulture);
                }
                catch (Exception)
                {
                    throw new ArgumentException("Invalid birthdate format");
                }
                
            }

            public User() { }
        }

    }