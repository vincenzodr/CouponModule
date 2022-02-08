from odoo import models, fields, api

import odoorpc
import datetime as dt
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class CouponProgramInherit(models.Model):
    _inherit = 'coupon.program'

    def invio(self, server, c):
        me = "vinidivelia2006@gmail.com"
        you = c['email']
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Vini di Velia - Codice sconto"
        msg['From'] = me
        msg['To'] = you

        # Create the body of the message (a plain-text and an HTML version).
        text = f"Ciao {c['nome']}, c'è un'offerta imperdibile per te."
        html = f"""
        <table border="0" cellpadding="0" cellspacing="0" style="box-sizing:border-box;border-collapse:collapse;width:100%; margin:0px auto;" width="100%"><tbody style="box-sizing:border-box;">
            <tr style="box-sizing:border-box;"><td valign="top" style="box-sizing:border-box;text-align: center; font-size: 14px;">
                <t t-if="{c["nome"]}" data-oe-t-group-active="true" style="box-sizing:border-box;" data-oe-t-group="10" data-oe-t-inline="true">
                    <br style="box-sizing:border-box;"><strong style="box-sizing:border-box;font-weight:bolder;font-size: 24px;">
                            Congratulazioni <t t-out="{c["nome"]} or ''" data-oe-t-inline="true" style="box-sizing:border-box;" contenteditable="false">{c["nome"]}</t>,<br style="box-sizing:border-box;">
                        </strong>
                </t>
                <br style="box-sizing:border-box;"><strong style="box-sizing:border-box;font-weight:bolder;font-size: 24px;">
                            per te che sei nostro cliente abbiamo riservato il <t t-out="object.program_id.company_id.name or ''" data-oe-t-inline="true" style="box-sizing:border-box;" contenteditable="false"></t><br style="box-sizing:border-box;">
                        </strong>

                <t t-if="object.program_id.reward_type == 'discount'" data-oe-t-group-active="true" style="box-sizing:border-box;" data-oe-t-group="11" data-oe-t-selectable="true" data-oe-t-inline="true">
                    <t t-else="" style="box-sizing:border-box;" data-oe-t-selectable="true" data-oe-t-group="12" data-oe-t-inline="true">
                        <span style="box-sizing:border-box;font-size: 50px; color: #875A7B; font-weight: bold;"><t t-out="object.program_id.discount_percentage or ''" data-oe-t-inline="true" style="box-sizing:border-box;" contenteditable="false">20</t> %</span>
                    </t>

                    <t t-else="" style="box-sizing:border-box;" data-oe-t-selectable="true" data-oe-t-group="13" data-oe-t-inline="true">
                        <br style="box-sizing:border-box;"><strong style="box-sizing:border-box;font-weight:bolder;font-size: 24px;">
                            di sconto sul tuo prossimo acquisto
                        </strong>
                    </t>
                    <br style="box-sizing:border-box;">
                </t>

            </td></tr>
            <tr style="box-sizing:border-box;margin-top: 16px"><td valign="top" style="box-sizing:border-box;text-align: center; font-size: 14px;">
                Usa questo codice promozionale
                <p style="box-sizing:border-box;font-size:13px;font-family:&quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;margin-top: 16px;">
                    <strong style="box-sizing:border-box;font-weight:bolder;padding: 16px 8px 16px 8px; border-radius: 3px; background-color: #F1F1F1;" t-out="{c["codice"]} or ''" contenteditable="false">{c["codice"]}</strong>
                </p>

                <t t-if="object.program_id.rule_minimum_amount != 0.00" data-oe-t-group-active="true" style="box-sizing:border-box;" data-oe-t-group="17" data-oe-t-inline="true">
                    <span style="box-sizing:border-box;font-size: 14px;">
                        Valido su una spesa minima di <t t-out="object.program_id.company_id.currency_id.symbol or ''" data-oe-t-inline="true" style="box-sizing:border-box;" contenteditable="false">€</t><t t-out="'%0.2f' % float(object.program_id.rule_minimum_amount) or ''" data-oe-t-inline="true" style="box-sizing:border-box;" contenteditable="false">20.00</t>
                    </span><br style="box-sizing:border-box;">
                </t>
                <br style="box-sizing:border-box;">
                Grazie,
                <t t-if="object.order_id.user_id.signature" data-oe-t-group-active="true" style="box-sizing:border-box;" data-oe-t-group="19" data-oe-t-inline="true">
                    <br style="box-sizing:border-box;">
                    <t t-out="object.order_id.user_id.signature or ''" data-oe-t-inline="true" style="box-sizing:border-box;" contenteditable="false"><br style="box-sizing:border-box;">Vini di Velia</t>
                </t>
            </td></tr>
        </tbody></table>  
        """
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        server.sendmail(me, you, msg.as_string())

    def test(self):
        username = 'vinidivelia2006@gmail.com'
        psw = 'vinidivelia'

        odoo = odoorpc.ODOO('localhost', port=8070)
        odoo.login('vinidivelia', username, psw)

        coupon = odoo.env['coupon.coupon']

        contatti = []
        data = dt.datetime.now() - dt.timedelta(days=60)
        POS = odoo.env['pos.order']
        POS_ids = POS.search([])  # 'date_order', '<', data
        for ordine in POS.browse(POS_ids):
            if ordine.partner_id.email:
                contatto = {
                    'id': ordine.partner_id.id,
                    'nome': ordine.partner_id.name,
                    'email': ordine.partner_id.email,
                    'data': ordine.date_order,
                    'codice': ''
                }
                contatti.append(contatto)

        sale = odoo.env['sale.order']
        sale_ids = sale.search([])
        for ordine in sale.browse(sale_ids):
            if ordine.partner_id.email:
                contatto = {
                    'id': ordine.partner_id.id,
                    'nome': ordine.partner_id.name,
                    'email': ordine.partner_id.email,
                    'data': ordine.date_order,
                    'codice': ''
                }
                contatti.append(contatto)

        contatti2 = [c for c in contatti if c['data'] < data]  # filtro data
        clienti = []
        for i in range(0, len(contatti2)):  # elimina duplicati
            ids = [c['id'] for c in clienti]
            if contatti2[i]['id'] not in ids:
                clienti.append(contatti2[i])

        for c in clienti:
            coupon_ids = coupon.search([('state', '=', 'new'), ('partner_id', '=', None)])
            if len(coupon_ids) > 0:
                c0 = coupon.browse(coupon_ids[0])
                c0.write({'partner_id': c['id'], 'state': 'sent'})
                c['codice'] = c0.code

        # configurazione server email
        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls
        sender_email = "vinidivelia2006@gmail.com"
        password = "Egidia.06"

        # Create a secure SSL context
        context = ssl.create_default_context()
        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()  # Can be omitted
            server.starttls(context=context)  # Secure the connection
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            # TODO: Send email here
            for c in clienti:
                if c["codice"] != '':
                    self.invio(server, c)
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit()