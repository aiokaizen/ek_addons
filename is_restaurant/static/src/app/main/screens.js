/** @odoo-module */
/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

import { PrintBillButton } from "@pos_restaurant/app/control_buttons/print_bill_button/print_bill_button";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { renderToString } from "@web/core/utils/render";
import { HWPrinter } from "@point_of_sale/app/printer/hw_printer";
import { customHtmlToCanvas as htmlToCanvas } from "@is_pos_network_printer/app/main/render_service";



patch(PrintBillButton.prototype, {
    // setup() {
    //     this.pos = usePos();
    //     onMounted(this.onMounted);
    //     this.classReceipt = "pos-bill-print-custom"
    //     this.isBillReceipt = true
    //     super.setup();
    // },


    async printBillOrder() {

        // ###############################
        // This function is not yet ready!
        // ###############################
        let self = this
        let order = this.pos.get_order().export_for_printing()
        let isPrintSuccessful = true
        console.log("this is order: ", order);
        order.currency = this.pos.currency.symbol
        const receiptXmlBill = renderToString('XmlBill', {
            data: order,
        })
        $("#id-bill-print-container").html(`
            <div class="pos-order-container">
                ${receiptXmlBill}
            </div>
        `);

        const receiptString = $("#id-bill-print-container")[0];
        const printer = new HWPrinter({ rpc: this.rpc, url: this.host });

        const ticketImage = printer.processCanvas(
            await htmlToCanvas(receiptString, { addClass: 'pos-order-print' })
        );
        const container = $("#id-bill-print-container")[0];
        try {
            const esc_commands = await this.env.services.orm.silent.call(
                'pos.order',
                'get_esc_command_set',
                [{ "data": "<receipt></receipt>" }]
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
            this.env.services.popup.add(ErrorPopup, {
                title: _t('Failed To Fetch Receipt Details.'),
                body: _t('Please make sure you are connected to the network.'),
            });
        }
        return isPrintSuccessful;

    },
    // /**
    //  * @override
    //  */
    async printReceipt() {
        // this.printNetworkPrinterOrder();
        this.printBillOrder()
        this.currentOrder._printed = false;

    },

    async click() {
        // await this.pos.showTempScreen("BillScreen");
        this.printBillOrder();
    }
});