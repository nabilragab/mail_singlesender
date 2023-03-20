# -*- coding: utf-8 -*-
#################################################################################
# Author      : Reson for IT Solutions (<https://reson.ae/>)
# Copyright(c): 2020-Present reson.ae
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
# You should have received a copy of the License along with this program.
# If not, see <https://reson.ae/license/>
#################################################################################
{
    'name': 'Mail Single Server',
    'description': 'This module removes multiple sender functionality and makes only one active email for sender '
                   'set using System Parameters: '
                   'single.sender.email.rfc = mail@server.com '
                   'single.sender.email = Company Name <mail@server.com>',
    'summary': 'Mail Single Server',
    'category': 'Mail',
    'version': '15.0.1.0.0',
    'author': 'Nabil Mohamed Ali Ragab',
    'company': 'Reson for IT Solutions',
    'maintainer': 'Reson for IT Solutions',
    'website': "https://www.reson.ae",
    'depends': ['mail', 'base', 'base_setup'],
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'Other proprietary',
    'images': ['static/description/banner.jpg'],
    'currency': 'USD',
    'price': 0.00,
    'support': 'nabil@reson.ae',

}
