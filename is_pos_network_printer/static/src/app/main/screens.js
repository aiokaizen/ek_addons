/** @odoo-module */
/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
// import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { renderToString } from "@web/core/utils/render";
import { onMounted } from "@odoo/owl";
import { HWPrinter } from "@point_of_sale/app/printer/hw_printer";
// import { htmlToCanvas } from "@point_of_sale/app/printer/render_service";
import { customHtmlToCanvas as htmlToCanvas } from "@is_pos_network_printer/app/main/render_service";

patch(ReceiptScreen.prototype, {
    setup() {
        this.pos = usePos();
        onMounted(this.onMounted);
        this.classReceipt = "pos-receipt-print-custom"
        super.setup();
    },
    onMounted() {
        this.printNetworkPrinterReceipt();
    },
    async printNetworkPrinterReceipt(event) {
        var self = this;
        var receipt = renderToString('XmlReceipt', {
            data: self.pos.get_order().export_for_printing(),
            formatCurrency: this.env.utils.formatCurrency,
        })
        receipt = "<receipt></receipt>"
        const printer = new HWPrinter({ rpc: this.rpc, url: this.host });
        const receiptString = $(".pos-receipt-container .d-inline-block")[0];

        const ticketImage = printer.processCanvas(
            await htmlToCanvas(receiptString, { addClass: "pos-receipt-print" })
        );

        // $(".pos-receipt-print").css("font-size", "34px")

        try {
            const esc_commands = await this.env.services.orm.silent.call(
                'pos.order',
                'get_esc_command_set',
                [{ "data": receipt }]
            );
            if (esc_commands) {
                // var esc = esc_commands.replace("\n", "\x0A")
                var printer_name = self.pos.config.printer_name;
                if (!qz.websocket.isActive()) {
                    self.pos.connect_to_nw_printer().finally(function () {
                        if (self.pos.nw_printer && self.pos.nw_printer.remote_status == "success") {
                            var config = qz.configs.create(printer_name);
                            // var data = [esc]
                            var wk_data = [{ type: 'raw', format: 'image', data: 'data:image/jpeg;base64,' + ticketImage + '', options: { language: "ESCPOS", dotDensity: 'double' } }, '\x1B' + '\x69',]
                            // { type: 'raw', format: 'image', data: receipt_data.receipt.company.logo, options: { language: "ESCPOS", dotDensity: 'double'} },
                            qz.print(config, wk_data).then(function () { }).catch(function (e) {
                                console.error(e);
                            });
                        }
                    })
                } else {
                    var config = qz.configs.create(printer_name);
                    // var data = [esc]
                    var wk_data = [
                        {
                            type: 'raw',
                            format: 'image',
                            data: 'data:image/jpeg;base64,' + ticketImage + '',
                            options: { language: "ESCPOS", dotDensity: 'double' },
                            // orientation: "landscape",
                            units: 'cm',
                            size: { width: 1.28, height: 20 },
                        },
                        '\x1B' + '\x64' + '\x02', // Add two line feeds
                        '\x1D' + '\x56' + '\x42' + '\x03', // Cut paper command with partial cut
                        // '\x1B' + '\x69',
                    ]
                    // { type: 'raw', format: 'image', data: receipt_data.receipt.company.logo, options: { language: "ESCPOS", dotDensity: 'double'} },
                    qz.print(config, wk_data).then(function () { });

                }
                return { successful: true };


            }
        } catch (event) {
            // event.preventDefault();
            self.env.services.popup.add(ErrorPopup, {
                title: _t('Failed To Fetch Receipt Details.'),
                body: _t('Please make sure you are connected to the network.'),
            });
        }
    }
});
