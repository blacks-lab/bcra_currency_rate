import requests
import logging
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

BCRA_API_URL = "https://api.estadisticasbcra.com/api/usd"

class ResCompany(models.Model):
    _inherit = 'res.company'

    bcra_api_key = fields.Char(string='API Key BCRA')

class CurrencyRate(models.Model):
    _inherit = 'res.currency.rate'

    @api.model
    def update_bcra_currency_rates(self):
        companies = self.env['res.company'].search([('bcra_api_key', '!=', False)])
        
        if not companies:
            raise UserError(_('Configure el API Key del BCRA en la configuración de la compañía'))

        for company in companies:
            headers = {
                'Authorization': f'Bearer {company.bcra_api_key}',
                'Accept': 'application/json'
            }
            
            try:
                response = requests.get(BCRA_API_URL, headers=headers, timeout=10)
                response.raise_for_status()
                rates = response.json()
                
                if not rates:
                    raise UserError(_('No se obtuvieron datos del BCRA'))
                
                latest_rate = rates[-1]
                rate_date = datetime.strptime(latest_rate['d'], '%Y-%m-%d').date()
                rate_value = latest_rate['v']
                
                currency = self.env.ref('base.ARS')
                usd_currency = self.env.ref('base.USD')
                
                self.create({
                    'name': rate_date.strftime('%Y-%m-%d'),
                    'rate': 1 / rate_value,
                    'currency_id': usd_currency.id,
                    'company_id': company.id
                })
                
                _logger.info(f'Tasa actualizada: 1 USD = {rate_value} ARS ({rate_date})')

            except requests.exceptions.RequestException as e:
                _logger.error(f'Error BCRA API: {str(e)}')
                raise UserError(_('Error conectando al BCRA: %s') % str(e))
