from django.core.management.base import BaseCommand
from categories.models import Category, SubCategory

class Command(BaseCommand):
    help = 'Populate categories and subcategories'

    def handle(self, *args, **kwargs):
        categories_data = {
            'Expenses': [
                'Housing', 'Transportation', 'Food', 'Health', 'Personal',
                'Education', 'Savings', 'Debt', 'Miscellaneous'
            ],
            'Incomes': [
                'Employment', 'Investments', 'Business', 'Government', 'Miscellaneous'
            ]
        }

        subcategories_data = {
            'Housing': [
                'Rent/Mortgage', 'Electricity', 'Water', 'Trash', 'Internet',
                'Maintenance', 'Property Tax'
            ],
            'Transportation': [
                'Fuel', 'Car Payment', 'Insurance', 'Public Transit', 'Maintenance',
                'Parking'
            ],
            'Food': [
                'Groceries', 'Dining Out', 'Snacks', 'Beverages'
            ],
            'Health': [
                'Insurance', 'Doctor Visits', 'Medication', 'Dental Care', 'Gym'
            ],
            'Personal': [
                'Clothing', 'Haircuts', 'Skincare', 'Entertainment', 'Hobbies'
            ],
            'Education': [
                'Tuition', 'Books', 'Supplies', 'Courses'
            ],
            'Savings': [
                'Emergency Fund', 'Retirement', 'Investments'
            ],
            'Debt': [
                'Credit Cards', 'Student Loans', 'Personal Loans'
            ],
            'Miscellaneous (Expenses)': [
                'Subscriptions', 'Donations', 'Gifts'
            ],
            'Employment': [
                'Salary', 'Bonuses', 'Overtime'
            ],
            'Investments': [
                'Dividends', 'Interest', 'Capital Gains'
            ],
            'Business': [
                'Sales', 'Freelance', 'Royalties'
            ],
            'Government': [
                'Tax Refund', 'Unemployment', 'Social Security'
            ],
            'Miscellaneous (Incomes)': [
                'Gifts', 'Inheritance'
            ]
        }

        # Loop through each category
        for category_type, category_names in categories_data.items():
            for category_name in category_names:
                # Check if category already exists, or create it
                category, created = Category.objects.get_or_create(
                    name=category_name,
                    category_type=category_type
                )

                # Get the subcategories for the category (including "Others")
                subcategories = subcategories_data.get(category_name, [])
                for sub_name in subcategories:
                    # Ensure "Others" subcategory is always created for each category
                    SubCategory.objects.get_or_create(
                        category=category, 
                        name=sub_name
                    )
                
                # Ensure the "Others" subcategory exists for each category
                SubCategory.objects.get_or_create(
                    category=category, 
                    name='Others'
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated categories and subcategories with "Others" subcategory'))
