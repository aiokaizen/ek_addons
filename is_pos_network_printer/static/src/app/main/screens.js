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
import { htmlToCanvas } from "@point_of_sale/app/printer/render_service";

patch(ReceiptScreen.prototype, {
    setup() {
        this.pos = usePos();
        onMounted(this.onMounted);
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
        try {
            const esc_commands = await this.env.services.orm.silent.call(
                'pos.order',
                'get_esc_command_set',
                [{ "data": receipt }]
            );
            if (esc_commands) {
                var esc = esc_commands.replace("\n", "\x0A")
                var printer_name = self.pos.config.printer_name;
                if (!qz.websocket.isActive()) {
                    self.pos.connect_to_nw_printer().finally(function () {
                        if (self.pos.nw_printer && self.pos.nw_printer.remote_status == "success") {
                            var config = qz.configs.create(printer_name);
                            // var data = [esc]
                            var wk_data = [{ type: 'raw', format: 'image', data: 'data:image/jpeg;base64,' + ticketImage + '', options: { language: "ESCPOS", dotDensity: 'double'} },'\x1B' + '\x69',]
                            // { type: 'raw', format: 'image', data: receipt_data.receipt.company.logo, options: { language: "ESCPOS", dotDensity: 'double'} },
                            qz.print(config, wk_data).then(function () { }).catch(function (e) {
                                console.error(e);
                            });
                        }
                    })
                } else {
                    var config = qz.configs.create(printer_name);
                    // var data = [esc]
                    var wk_data = [{ type: 'raw', format: 'image', data: 'data:image/jpeg;base64,' + ticketImage + '', options: { language: "ESCPOS", dotDensity: 'double'} },'\x1B' + '\x69',]
                    // { type: 'raw', format: 'image', data: receipt_data.receipt.company.logo, options: { language: "ESCPOS", dotDensity: 'double'} },
                    qz.print(config, wk_data).then(function () { });
                }
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

// patch(PaymentScreen.prototype, {
//     setup() {
//         super.setup();
//     },
//     async afterOrderValidation(suggestToSync = true) {
//         // Remove the order from the local storage so that when we refresh the page, the order
//         // won't be there
//         this.pos.db.remove_unpaid_order(this.currentOrder);

//         // Ask the user to sync the remaining unsynced orders.
//         if (suggestToSync && this.pos.db.get_orders().length) {
//             const { confirmed } = await this.popup.add(ConfirmPopup, {
//                 title: _t("Remaining unsynced orders"),
//                 body: _t("There are unsynced orders. Do you want to sync these orders?"),
//             });
//             if (confirmed) {
//                 // NOTE: Not yet sure if this should be awaited or not.
//                 // If awaited, some operations like changing screen
//                 // might not work.
//                 this.pos.push_orders();
//             }
//         }
//         // Always show the next screen regardless of error since pos has to
//         // continue working even offline.
//         let nextScreen = this.nextScreen;

//         if (
//             nextScreen === "ReceiptScreen" &&
//             !this.currentOrder._printed &&
//             this.pos.config.iface_print_auto
//         ) {
//             const invoiced_finalized = this.currentOrder.is_to_invoice()
//                 ? this.currentOrder.finalized
//                 : true;

//             if (invoiced_finalized) {
//                 const printResult = await this.printer.print(
//                     OrderReceipt,
//                     {
//                         data: this.pos.get_order().export_for_printing(),
//                         formatCurrency: this.env.utils.formatCurrency,
//                     },
//                     { webPrintFallback: true }
//                 );
//                 // const printResult = await this.printNetworkPrinterReceipt();

//                 if (printResult && this.pos.config.iface_print_skip_screen) {
//                     this.pos.removeOrder(this.currentOrder);
//                     this.pos.add_new_order();
//                     nextScreen = "ProductScreen";
//                 }
//             }
//         }

//         this.pos.showScreen(nextScreen);
//     },
//     async printNetworkPrinterReceipt(event) {

//         // alert("Function overridden");
//         // return { successful: true };
//         // return false;

//         var self = this;
//         console.log("self:", self);
//         var receipt = renderToString('XmlReceipt', {
//             data: self.pos.get_order().export_for_printing(),
//             formatCurrency: this.env.utils.formatCurrency,
//         })
//         // receipt = "<receipt></receipt>"
//         console.log("receipt:", receipt);
//         const printer = new HWPrinter({ rpc: this.rpc, url: this.host });
//         const receiptString = $(".pos-receipt-container .d-inline-block")[0];
//         const ticketImage = printer.processCanvas(
//             await htmlToCanvas(receiptString, { addClass: "pos-receipt-print" })
//         );
//         console.log("printer:", printer);
//         try {
//             const esc_commands = await this.env.services.orm.silent.call(
//                 'pos.order',
//                 'get_esc_command_set',
//                 [{ "data": receipt }]
//             );
//             console.log("esc_commands:", esc_commands);
//             if (esc_commands) {
//                 var esc = esc_commands.replace("\n", "\x0A")
//                 console.log("esc:", esc);
//                 var printer_name = self.pos.config.printer_name;
//                 console.log("printer_name:", printer_name);
//                 if (!qz.websocket.isActive()) {
//                     self.pos.connect_to_nw_printer().finally(function () {
//                         console.log("self.pos.nw_printer:", self.pos.nw_printer)
//                         if (self.pos.nw_printer && self.pos.nw_printer.remote_status == "success") {
//                             var config = qz.configs.create(printer_name);
//                             // var data = [esc]
//                             var wk_data = [{ type: 'raw', format: 'image', data: 'data:image/jpeg;base64,' + ticketImage + '', options: { language: "ESCPOS", dotDensity: 'double'} },'\x1B' + '\x69',]
//                             // { type: 'raw', format: 'image', data: receipt_data.receipt.company.logo, options: { language: "ESCPOS", dotDensity: 'double'} },
//                             qz.print(config, wk_data).then(function () { }).catch(function (e) {
//                                 console.error(e);
//                             });
//                         }
//                     })
//                 } else {
//                     var config = qz.configs.create(printer_name);
//                     // var data = [esc]
//                     var wk_data = [{ type: 'raw', format: 'image', data: 'data:image/jpeg;base64,' + ticketImage + '', options: { language: "ESCPOS", dotDensity: 'double'} },'\x1B' + '\x69',]
//                     // { type: 'raw', format: 'image', data: receipt_data.receipt.company.logo, options: { language: "ESCPOS", dotDensity: 'double'} },
//                     qz.print(config, wk_data).then(function () { });
//                 }
//             }
//             return { successful: true };
//         } catch (event) {
//             // event.preventDefault();
//             self.env.services.popup.add(ErrorPopup, {
//                 title: _t('Failed To Fetch Receipt Details.'),
//                 body: _t('Please make sure you are connected to the network.'),
//             });
//             return { successful: false };
//         }
//     }
// })
