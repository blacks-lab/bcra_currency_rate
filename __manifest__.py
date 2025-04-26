{
    'name': 'BCRA Argentina Currency Rate',
    'version': '18.0',
    'category': 'Financial',
    'summary': 'Actualización de tasas de cambio del BCRA Argentina',
    'author': 'Ernesto Bernís',
    'website': 'https://github.com/blacks-lab/bcra_currency_rate',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_company_views.xml',
    ],
    'installable': True,
    'application': False,
}
