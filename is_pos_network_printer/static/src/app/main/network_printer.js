/* @odoo-module */
/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
import { BasePrinter } from "@point_of_sale/app/printer/base_printer";

export class NetworkPrinter extends BasePrinter {
    setup(params) {
        super.setup(...arguments);
        this.remote_status = 'disconnected';
        this.config = false;
        this.printer_name = false;
        this.remote_status = 'disconnected'
        this.printer_id = false;
        if(params && params.pos){
            this.pos = params.pos
            this.printer_name = params.printer_name;
            this.printer_id = params.printer_id;
        }
    }
    connect_to_printer(){
        var self = this;
        self.set_status('connecting')
        return qz.websocket.connect().then(function () {
            if(self.pos){
                var printer_name = self.pos.config.printer_name
                self.remote_status = 'connected';
                self.set_status(self.remote_status)
                return qz.printers.find(printer_name).then(function (found) {
                    self.config = qz.configs.create(printer_name);
                    self.remote_status = 'success';
                    self.set_status(self.remote_status)
                }).catch(function (e) {
                    self.remote_status = 'c_error';
                    self.set_status(self.remote_status)
                });
            }
        }).catch(function (e) {
            console.error(e);
            self.remote_status = 'c_error';
            self.set_status(self.remote_status)
        });
    }
    connect_to_kitchen_printer(printer){
        var self = this
        return qz.websocket.connect().then(function(){
            var printer_name = printer.printer_name
            self.remote_status = 'connected';
            return qz.printers.find(printer_name).then(function(found){
                self.config = qz.configs.create(printer_name);
                self.remote_status = 'success';
            }).catch(function(e){
                self.remote_status = 'c_error';
            });
        }).catch(function(e){
            console.error(e);
            self.remote_status = 'c_error';
        });
    }
    set_status(status){
        var status_list = ['connected', 'connecting', 'c_error', 'success']
        for (var i = 0; i < status_list.length; i++) {
            $('.nw_printer .js_' + status_list[i]).addClass('d-none');
        }
        $('.nw_printer .js_' + status).removeClass('d-none');
    }
    disconnect_from_printer(){
        return qz.websocket.disconnect();
    }
};
