/* @odoo-module */
/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
import { BasePrinter } from "@point_of_sale/app/printer/base_printer";


const CERTIFICATE = "-----BEGIN CERTIFICATE-----\n" +
    "MIIDYTCCAkkCFGnjtA4J8rNLjECwy124j6jC18zDMA0GCSqGSIb3DQEBCwUAMG0x\n" +
    "CzAJBgNVBAYTAk1BMRIwEAYDVQQIDAlNYXJyYWtlY2gxEjAQBgNVBAcMCU1hcnJh\n" +
    "a2VjaDERMA8GA1UECgwIRUtCbG9ja3MxCzAJBgNVBAsMAklUMRYwFAYDVQQDDA0x\n" +
    "OTIuMTY4LjEwMC41MB4XDTI0MDUxNjIxMzkyMVoXDTI1MDUxNjIxMzkyMVowbTEL\n" +
    "MAkGA1UEBhMCTUExEjAQBgNVBAgMCU1hcnJha2VjaDESMBAGA1UEBwwJTWFycmFr\n" +
    "ZWNoMREwDwYDVQQKDAhFS0Jsb2NrczELMAkGA1UECwwCSVQxFjAUBgNVBAMMDTE5\n" +
    "Mi4xNjguMTAwLjUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDDsUiy\n" +
    "1nYKCFN4ux1E88TdKUMgun7i54efwE2nA44oXBDIrJE10nN5zG5fYUdWv2WMEBYV\n" +
    "268lMgGUmXyg+Y5yukfVUG5gdAtyn3qaZ5siMEd6r4rEjkfSn8pBXmOgARrbdmGF\n" +
    "UtxoZERiVDXBlXlSeZrgpZQ/JmGiZNGu931yopvyC+Jhv6LwX0eI6IUQfUM7n2kY\n" +
    "KYQzjkM8T5byk4JJ1fZr+b9Wjz2Mh7lNdcKBaJT9b57wx13qoNoC7TTkIMDRzjRc\n" +
    "OBxAlM+Z9yAjmSNplNqg/5TS9ct/cbxRyDDvSgqKjSVjFNUQ9q8NnHhTM6QNODD4\n" +
    "bNwfACCqmE0/D3kPAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAGxKR6NFjA7p4mPC\n" +
    "UODLRIfoYx6be0exffWe19/SvBnVMMi+1C5eIiLT7KseQ7Xh6l824bWL5X1T7DaK\n" +
    "Vh/dCIEURlm47ykdr3KFaiiqT+npQRQA3MHhU/gPo6mZKMU5VsVmrMzcooXEQymZ\n" +
    "lJTTR5kvRdDqPqx/In+kHiwcio7KGYktoupYi6aotUiKb8w2GsvsDnRMwXg80ao9\n" +
    "XUiBCTPEPRHkxFxvag+J3fa4Ff1q3OvNXfP4u3bdlvbHgbN3eyDhA/SUW7Jd8ZdM\n" +
    "OwBaCV4AqHhS/d8XOulzyhVqrY5Gz/QRqjAJ9sPI68YJuoL8lDFD3Oa+4JW6QbPV\n" +
    "LLYBpdI=\n" +
    "-----END CERTIFICATE-----";

const PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\n" +
    "MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDDsUiy1nYKCFN4\n" +
    "ux1E88TdKUMgun7i54efwE2nA44oXBDIrJE10nN5zG5fYUdWv2WMEBYV268lMgGU\n" +
    "mXyg+Y5yukfVUG5gdAtyn3qaZ5siMEd6r4rEjkfSn8pBXmOgARrbdmGFUtxoZERi\n" +
    "VDXBlXlSeZrgpZQ/JmGiZNGu931yopvyC+Jhv6LwX0eI6IUQfUM7n2kYKYQzjkM8\n" +
    "T5byk4JJ1fZr+b9Wjz2Mh7lNdcKBaJT9b57wx13qoNoC7TTkIMDRzjRcOBxAlM+Z\n" +
    "9yAjmSNplNqg/5TS9ct/cbxRyDDvSgqKjSVjFNUQ9q8NnHhTM6QNODD4bNwfACCq\n" +
    "mE0/D3kPAgMBAAECggEAZqDZIYE7knNfY1euN/Un71yuacGkvdby16MAlnBU43G1\n" +
    "E6j81p8yFFRUJg1cXnAuD1B4ZKo7pmQdVBNSuxFl1WFAPuzZlhgF0O02XTessjdj\n" +
    "pUHeosqDfEB0z+dyk/1AWowxBLy5/r1m57KGJqn/YHOJ9/qeTqgQWBxLo1kEH1Of\n" +
    "18DhTnEbTrvL0kERpbG8QuvTwUWUI6JcSg0L9ogGbGWrgmJ5CYVmaoVJt7L8ftlK\n" +
    "WdTl8JS1KemvFNeBtrGZ4yYKgGdEWIi7Xkw5im9ytP+8utLcaFhcdNCihDHvN9um\n" +
    "H1RDLmFVoOoFq4kdYls6LZZ2muEcbWTf2yyDjaQMgQKBgQD7p6mwUX6C5EnVaf4a\n" +
    "F+RVcQnphbzRt6FDO4/5nmLreZNMBVX2LEepUqXnUOan1+/wel3AGMCeXki7sxfD\n" +
    "8/GaKMUMp62xa5mdeX4BuLNHtCtgzc/rIngc5raHJZEUZ3QssgeUiyHWkuiF58BJ\n" +
    "izSa++Oh8e44QSNhLpN7hZBh4QKBgQDHEkMklkbr/9DIX1KL7ov0RDrYx7rhKU4N\n" +
    "ezv1EtpYTcO3b2YxNC7C9SpwoRKzQ+CVPAhxTByS5e098tRGa+gPQIGNjP3cev8/\n" +
    "mcezPuaI9D43xMyLvPBZ1yfACJ+pM6mbzScWSJRTT/t9pTTL4sp2AFQQz3flpZKk\n" +
    "diHCFPcY7wKBgQDxDoyr+ZQ+22CiTlJ6OjKdaZc+Gr5hAQ43McHbMU2+FAn1gxLx\n" +
    "qT7HwgRrTIJ1epI6/2v4S32O9e+j5Iy6Rl1C9xSx55io39IZFzyNd5g78iivJNaq\n" +
    "fK0juhhT4rdTHToaajp6nr++I6EaS4FUsUSlxO0qvm0bc8HpIE1jv/Aq4QKBgQDG\n" +
    "Y0zGiXzkdGx9Q4HgMjsHk3eR0npLKf6/MLDv63ntxpHlnP8aygZQBEPnOp6ISHzo\n" +
    "PIutXUycmMd1lSo3hBIgIQj7KCdWMr1thLOfzm+wzLe0nEu8du6QmfrjRbTXysSc\n" +
    "oDbz3iDzZiIbdSjIh5t9PZaJqjiyg+9ANvotkPcvwQKBgQCbORpyzA84SeyIOj89\n" +
    "vkFbt0CAbCNqlSU/1PR40HM1F56XOJjFjBDq4SlMGyah1I8I5EEGLULXhKndPFHs\n" +
    "wIfmEEGK+qk1ei3qR3cID92fvF808vY90P3tEG6oUcacM1i2BWAYFjRcmiO7HUHw\n" +
    "QF5ZQMRnOIcicKc41K2Bk9j0bg==\n" +
    "-----END PRIVATE KEY-----\n";


export class NetworkPrinter extends BasePrinter {

    // constructor() {
    //     super();
    //     // Fix certificate problems
    //     qz.security.setSignatureAlgorithm("SHA512");
    //     qz.security.setSignaturePromise(function(toSign) {
    //         return function(resolve, reject) {
    //             try {
    //                 var pk = KEYUTIL.getKey(PRIVATE_KEY);
    //                 var sig = new KJUR.crypto.Signature({"alg": "SHA512withRSA"});
    //                 sig.init(pk);
    //                 sig.updateString(toSign);
    //                 var hex = sig.sign();
    //                 console.log("DEBUG: \n\n" + stob64(hextorstr(hex)));
    //                 resolve(stob64(hextorstr(hex)));
    //             } catch (err) {
    //                 console.error(err);
    //                 reject(err);
    //             }
    //         };
    //     });
    //     qz.security.setCertificatePromise(function(resolve, reject) {
    //         resolve(CERTIFICATE);
    //     });
    // }

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
    set_certificate() {

        qz.security.setSignatureAlgorithm("SHA512");

        qz.security.setSignaturePromise(function(toSign) {
            return function(resolve, reject) {
                try {
                    var pk = KEYUTIL.getKey(PRIVATE_KEY);
                    var sig = new KJUR.crypto.Signature({"alg": "SHA512withRSA"});  // Use "SHA1withRSA" for QZ Tray 2.0 and older
                    sig.init(pk);
                    sig.updateString(toSign);
                    var hex = sig.sign();
                    console.log("DEBUG: \n\n" + stob64(hextorstr(hex)));
                    resolve(stob64(hextorstr(hex)));
                } catch (err) {
                    console.error(err);
                    reject(err);
                }
            };
        });

        qz.security.setCertificatePromise(function(resolve, reject) {
            resolve(CERTIFICATE);
        });
    }
    connect_to_printer(){
        var self = this;
        self.set_status('connecting')

        // Set signing certificate
        // this.set_certificate();

        // Connect to QZ-Lib
        return qz.websocket.connect({host: self.pos.config.qz_server_host}).then(function () {
            if(self.pos){
                var printer_name = self.printer_name | self.pos.config.printer_name
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
        return qz.websocket.connect({host: self.pos.config.qz_server_host}).then(function(){
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
