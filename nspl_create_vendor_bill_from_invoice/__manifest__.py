{
    'name': 'Create Vendor Bill from Customer Invoice',
    'version': '19.0.1',
    'summary': 'Generate Vendor Bill directly from Customer Invoice',
    'description': """
    This module allows users to generate a vendor bill directly from a posted customer invoice:

    ✔ Add a "Generate Vendor Bill" button on posted customer invoices 
    ✔ View related vendor bills through a smart button  
    """,
    'category': 'Accounting',
    'sequence': 10,
    'author': 'Namah Softech Private Limited',
    'maintainer': 'Namah Softech Private Limited',
    'company': 'Namah Softech Private Limited',
    'website': 'https://www.namahsoftech.com',
    'support': 'support@namahsoftech.com',
    'price': 24.99,
    'currency': 'USD',
    'contributors': ['Rutik Patil'],
    'license': 'AGPL-3',
    'depends': ['account'],
    'data': [
        'views/account_move_views.xml',
        'views/account_move_vendor_bill_views.xml',
    ],
    'images': ['static/description/img/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
