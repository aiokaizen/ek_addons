/** @odoo-module **/
/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { NetworkPrinter } from "@is_pos_network_printer/app/main/network_printer";
import { renderToString } from "@web/core/utils/render";
import { htmlToCanvas } from "@point_of_sale/app/printer/render_service";
import { patch } from "@web/core/utils/patch";

patch(PosStore.prototype, {
    async setup(...args) {

        // Setting certification signing functions for QZ printing purposes.
        qz.security.setCertificatePromise(function(resolve, reject) {
            fetch(
                "is_pos_network_printer/static/src/app/main/qzlib/certificate.txt",
                {cache: 'no-store', headers: {'Content-Type': 'text/plain'}}
            ).then(function(data) { data.ok ? resolve(data.text()) : reject(data.text()); });
        });
        qz.security.setSignatureAlgorithm("SHA1"); // Lower than 2.1; SHA512
        qz.security.setSignaturePromise(function(toSign) {
            return function(resolve, reject) {
                fetch("/qz-sign-message?request=" + toSign, {cache: 'no-store', headers: {'Content-Type': 'text/plain'}})
                    .then(function(data) { data.ok ? resolve(data.text()) : reject(data.text()); });
            };
        });

        // Continue setup function
        this.nw_printer = new NetworkPrinter({ pos: this, printer_name: this.config && this.config.printer_name || false });
        return await super.setup(...args);
    },
    connect_to_nw_printer(resolve = null) {
        var self = this;
        if(self.config.iface_network_printer){
            return self.nw_printer.disconnect_from_printer().finally(function (e) {
                return self.nw_printer.connect_to_printer();
            })
        }
    },
    connect_to_nw_preparation_printer(resolve = null, printer) {
        var self = this;
        if(self.config.iface_network_printer){
            return printer.disconnect_from_printer().finally(function (e) {
                return printer.connect_to_printer();
            })
        }
    },
    async after_load_server_data() {
        if (this.config.iface_network_printer) {
            this.connect_to_nw_printer()
        }
        return await super.after_load_server_data(...arguments);
    },
    async sendOrderInPreparation(order, cancelled = false) {

        if (this.printers_category_ids_set.size) {
            try {
                const changes = order.changesToOrder(cancelled);

                if (changes.cancelled.length > 0 || changes.new.length > 0) {
                    const isPrintSuccessful = await this.printNetworkPrinterOrder(order, cancelled);
                    if (!isPrintSuccessful) {
                        this.popup.add(ErrorPopup, {
                            title: _t("Printing failed"),
                            body: _t("Failed in printing the changes in the order"),
                        });
                    }
                }
            } catch (e) {
                console.warn("Failed in printing the changes in the order. e:", e);
            }
        }
    },
    async printNetworkPrinterOrder(order, cancelled = false) {

        // ###############################
        // This function is not yet ready!
        // ###############################

        const orderChange = order.changesToOrder(cancelled);
        let isPrintSuccessful = true;
        const d = new Date();
        let hours = "" + d.getHours();
        hours = hours.length < 2 ? "0" + hours : hours;
        let minutes = "" + d.getMinutes();
        minutes = minutes.length < 2 ? "0" + minutes : minutes;
        for (const printer of order.pos.unwatched.printers) {
            const changes = order._getPrintingCategoriesChanges(
                printer.config.product_categories_ids,
                orderChange
            );

            if (changes["new"].length > 0 || changes["cancelled"].length > 0) {
                const printingChanges = {
                    new: changes["new"],
                    cancelled: changes["cancelled"],
                    table_name: order.pos.config.module_pos_restaurant
                        ? order.getTable().name
                        : false,
                    floor_name: order.pos.config.module_pos_restaurant
                        ? order.getTable().floor.name
                        : false,
                    name: order.name.replace("Order", "Commande") || "unknown order",
                    printer: {
                        obj: printer,
                        name: printer.config.name
                    },
                    time: {
                        date: new Date().toLocaleDateString('fr-FR'),
                        hours,
                        minutes,
                    },
                    server: "Mohamed",  // Get current employee
                };
                console.log(`Printing Changes:`, printingChanges);

                const receipt = renderToString('XmlOrder', {
                    data: printingChanges,
                })
                $("#id-order-print-container").append(`
                    <div class="pos-order-container">
                        ${receipt}
                    </div>
                `);
                const receiptString = $("#id-order-print-container .order-receipt")[0];
                console.log("receipt:", receipt);
                console.log("receipt string:", receiptString);
                const ticketImage = printer.processCanvas(
                    await htmlToCanvas(receiptString, { addClass: 'pos-order-print'})
                );
                const container = $("#id-order-print-container")[0];
                console.log("container:", container);

                try {
                    var printer_obj = new NetworkPrinter(
                        { pos: order.pos, printer_name: printer.config.nw_printer_name }
                        // { pos: order.pos, printer_name: "POS-80" }
                    );
                    console.log("printer config:", printer.config);
                    console.log("Printer:", printer_obj)
                    if (!qz.websocket.isActive()) {
                        console.log("QZ websocket is NOT active.")
                        order.pos.connect_to_nw_preparation_printer(null, printer_obj).finally(function () {
                            if (printer_obj && printer_obj.remote_status == "success") {
                                var config = qz.configs.create(printer_obj.printer_name);
                                var wk_data = [{ type: 'raw', format: 'image', data: 'data:image/jpeg;base64,' + ticketImage + '', options: { language: "ESCPOS", dotDensity: 'double'} },'\x1B' + '\x69',]
                                qz.print(config, wk_data).then(function () { });
                            }
                        })
                    } else {
                        console.log("Printer name:", printer_obj.printer_name);
                        var config = qz.configs.create(printer_obj.printer_name);
                        var wk_data = [{ type: 'raw', format: 'image', data: 'data:image/jpeg;base64,' + ticketImage + '', options: { language: "ESCPOS", dotDensity: 'double'} },'\x1B' + '\x69',]
                        qz.print(config, wk_data).then(function () { });
                    }
                } catch (event) {
                    console.log("Error Event:", event)
                    isPrintSuccessful = false;
                    order.env.services.popup.add(ErrorPopup, {
                        title: _t('Failed To Fetch Receipt Details.'),
                        body: _t('Please make sure you are connected to the network.'),
                    });
                }
            }
        }

        return isPrintSuccessful;

    }
});
