# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# Copyright 2016 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo.exceptions import ValidationError


def pre_init_hook(cr):
    """Make sure there are no duplicates before installing the module.

    If you define a unique key in Odoo that cannot be applied, Odoo will log a
    warning and install the module without that constraint. Since this module
    is useless without those constraints, we check here if all will work before
    installing, and provide a user-friendly message in case of failure.
    """
    errors = list()

    # Search for duplicates in emails
    cr.execute(
        """SELECT LOWER(c.email) AS e, l.name, COUNT(c.id)
                  FROM
                    mailing_contact AS c
                    INNER JOIN mailing_contact_list_rel AS cl
                      ON cl.contact_id = c.id
                    INNER JOIN mailing_list AS l ON cl.list_id = l.id
                  GROUP BY l.name, e
                  HAVING COUNT(c.id) > 1"""
    )
    for result in cr.fetchall():
        errors.append("{0} appears {2} times in list {1}.".format(*result))

    # Search for duplicates in list's name
    cr.execute(
        """SELECT name, COUNT(id)
                  FROM mailing_list
                  GROUP BY name
                  HAVING COUNT(id) > 1"""
    )
    for result in cr.fetchall():
        errors.append("There are {1} lists with name {0}.".format(*result))

    # Abort if duplicates are found
    if errors:
        raise ValidationError("Fix this before installing:" + "".join("\n" + e for e in errors))
