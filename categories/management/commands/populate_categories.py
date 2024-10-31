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
                'Maintenance', 'Property Tax', 'Others'
            ],
            'Transportation': [
                'Fuel', 'Car Payment', 'Insurance', 'Public Transit', 'Maintenance',
                'Parking', 'Others'
            ],
            'Food': [
                'Groceries', 'Dining Out', 'Snacks', 'Beverages', 'Others'
            ],
            'Health': [
                'Insurance', 'Doctor Visits', 'Medication', 'Dental Care', 'Gym', 'Others'
            ],
            'Personal': [
                'Clothing', 'Haircuts', 'Skincare', 'Entertainment', 'Hobbies', 'Others'
            ],
            'Education': [
                'Tuition', 'Books', 'Supplies', 'Courses', 'Others'
            ],
            'Savings': [
                'Emergency Fund', 'Retirement', 'Investments', 'Others'
            ],
            'Debt': [
                'Credit Cards', 'Student Loans', 'Personal Loans', 'Others'
            ],
            'Miscellaneous (Expenses)': [
                'Subscriptions', 'Donations', 'Gifts', 'Others'
            ],
            'Employment': [
                'Salary', 'Bonuses', 'Overtime', 'Others'
            ],
            'Investments': [
                'Dividends', 'Interest', 'Capital Gains', 'Others'
            ],
            'Business': [
                'Sales', 'Freelance', 'Royalties', 'Others'
            ],
            'Government': [
                'Tax Refund', 'Unemployment', 'Social Security', 'Others'
            ],
            'Miscellaneous (Incomes)': [
                'Gifts', 'Inheritance', 'Others'
            ]
        }

        for category_type, category_names in categories_data.items():
            for category_name in category_names:
                category = Category.objects.create(name=category_name, category_type=category_type)
                subcategories = subcategories_data.get(category_name, [])
                for sub_name in subcategories:
                    SubCategory.objects.create(category=category, name=sub_name)

        self.stdout.write(self.style.SUCCESS('Successfully populated categories and subcategories'))
