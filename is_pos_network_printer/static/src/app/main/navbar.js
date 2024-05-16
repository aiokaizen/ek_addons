/** @odoo-module */
/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
import { Component } from "@odoo/owl";
import { Navbar } from "@point_of_sale/app/navbar/navbar";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { patch } from "@web/core/utils/patch";

export class SynchNetworkPrinterWidget extends Component {
    static template = "point_of_sale.SynchNetworkPrinterWidget";
    setup() {
        this.pos = usePos();
        super.setup();
    }
    onClick() {
        var self = this;
        if(this.pos.config.iface_network_printer){
            self.pos.nw_printer.disconnect_from_printer().finally(function (e) {
                self.pos.nw_printer.connect_to_printer();
            });
        }
    }
}
patch(Navbar, {
    components: { ...Navbar.components, SynchNetworkPrinterWidget},
});
