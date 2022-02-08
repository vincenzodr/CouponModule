{
    'name': "Invio buoni sconto",
    'version': '1.0',
    'depends': ['base','coupon'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
    Modulo invio sconti
    """,
    # data files always loaded at installation
    'data': [
        'views/mail.xml',
    ],    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
}