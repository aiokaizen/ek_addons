/** @odoo-module **/
/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { NetworkPrinter } from "@odoo_pos_network_printer/app/main/network_printer";
import { patch } from "@web/core/utils/patch";

patch(PosStore.prototype, {
    async setup(...args) {
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
    async after_load_server_data() {
        if (this.config.iface_network_printer) {
            this.connect_to_nw_printer()
        }
        return await super.after_load_server_data(...arguments);
    }
});
