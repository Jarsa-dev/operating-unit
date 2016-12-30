# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp.tests import common


class TestSaleTeamOperatingUnit(common.TransactionCase):

    def setUp(self):
        super(TestSaleTeamOperatingUnit, self).setUp()
        self.res_users_model = self.env['res.users']
        self.crm_team_model = self.registry('crm.team')
        # Groups
        self.grp_sale_mngr = self.env.ref('base.group_sale_manager')
        self.grp_user = self.env.ref('base.group_user')
        # Company
        self.company = self.env.ref('base.main_company')
        # Main Operating Unit
        self.ou1 = self.env.ref('operating_unit.main_operating_unit')
        # B2C Operating Unit
        self.b2c = self.env.ref('operating_unit.b2c_operating_unit')
        # Create User 1 with Main OU
        self.user1 = self._create_user('user_1', [self.grp_sale_mngr,
                                                  self.grp_user], self.company,
                                       [self.ou1])
        # Create User 2 with B2C OU
        self.user2 = self._create_user('user_2', [self.grp_sale_mngr,
                                                  self.grp_user], self.company,
                                       [self.b2c])
        # Create CRM teams
        self.team1 = self._create_crm_team(self.user1.id, self.ou1)
        self.team2 = self._create_crm_team(self.user2.id, self.b2c)

    def _create_user(self, login, groups, company, operating_units,
                     context=None):
        """ Create a user. """
        group_ids = [group.id for group in groups]
        user = self.res_users_model.create({
            'name': 'Test User',
            'login': login,
            'password': 'demo',
            'email': 'test@yourcompany.com',
            'company_id': company.id,
            'company_ids': [(4, company.id)],
            'operating_unit_ids': [(4, ou.id) for ou in operating_units],
            'groups_id': [(6, 0, group_ids)]
        })
        return user

    def _create_crm_team(self, uid, operating_unit):
        """Create a sale order."""
        context = {'mail_create_nosubscribe': True}
        crm = self.crm_team_model.create(self.cr, uid,
                                         {'name': 'CRM team',
                                          'operating_unit_id':
                                              operating_unit.id},
                                         context=context)
        return crm

    def test_crm_team(self):
        # User 2 is only assigned to B2C Operating Unit, and cannot
        # access CRM teams for Main Operating Unit.

        team = self.crm_team_model.search(
            self.cr, self.user2.id, [('id', '=', self.team1),
                                     ('operating_unit_id', '=', self.ou1.id)])
        self.assertEqual(team, [], 'User 2 should not have access to '
                         '%s' % self.ou1.name)
