# -*- coding: utf-8 -*-

{
    'name': 'Real Estate',
    'description': 'This is a test module',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',

        'views/res_users_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menu_views.xml',
    ]
}
