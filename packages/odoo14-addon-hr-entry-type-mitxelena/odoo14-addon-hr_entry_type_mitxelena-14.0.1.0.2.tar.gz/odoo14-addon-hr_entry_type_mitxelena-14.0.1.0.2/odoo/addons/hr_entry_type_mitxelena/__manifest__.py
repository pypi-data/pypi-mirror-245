{
    "name": "Entry Types Data for Mitxelena",
    "license": "AGPL-3",
    "version": "14.0.1.0.2",
    "category": "Human Resources",
    "sequence": 20,
    "summary": "Entry Types Data Customizations for Mitxelena",
    "website": "https://git.coopdevs.org/coopdevs/odoo/odoo-addons/odoo-mitxelena",
    "description": """
        ## Entry Type data for Mitxelena

        This module adds the entry type data customizations for Mitxelena.
        It depends on the [hr_entry_type](https://pypi.org/project/odoo14-addon-hr-entry-type) module.
    """,
    "author": "Coopdevs Treball SCCL",
    "depends": [
        "hr_entry_type",
    ],
    "data": [
        "data/hr_entry_type.xml",
    ],
    "demo": [],
    "installable": True,
    "application": False,
    "auto_install": False,
}
