# -*- coding: utf-8 -*-
{
    'name': 'Mail Single Server',
    'summary': 'Mail Single Server',
    'sequence': '9010',
    'category': 'Mail',
    'description': """
    This module removes multiple sender functionality and makes only one active email for sender
    set using System Parameters: 
    single.sender.email.rfc = mail@server.com
    single.sender.email = Company Name <mail@server.com>
    """,
    'depends': ['mail', 'base'],
}
