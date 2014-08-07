
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp.osv import orm, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta


class StockProductionLot(orm.Model):
    _inherit = "stock.production.lot"
    _columns = {
        "warrant_limit": fields.datetime("Warranty")
        }

    def create(self, cr, uid, values, context=None):
        if values['product_id']:
            product = self.pool["product.product"].browse(
                cr, uid, values["product_id"], context=context)
            create_date = ('create_date' in values and
                           values['create_date'] or datetime.now())
            if not product.seller_ids:
                warrant_limit = (
                    product.warranty and
                    (create_date +
                     relativedelta(months=int(product.warranty))))
                if warrant_limit:
                    values.update({'warrant_limit': warrant_limit})
            # else: TODO how get supplier warrant?
        return super(StockProductionLot, self).create(cr, uid, values,
                                                      context=context)
