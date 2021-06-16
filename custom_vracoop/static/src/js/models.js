/*
    Copyright 2019 Coop IT Easy SCRLfs
            Pierrick Brun <pierrick.brun@akretion.com>
    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/


odoo.define('custom_vracoop.models', function (require) {
    "use strict";

    var models = require('point_of_sale.models');

    models.Orderline = models.Orderline.extend({
        get_quantity_str: function(){
            if (this.product.to_weight){
                return 'NET' + this.quantityStr;
            } else {
                return this.quantityStr;
            }
        }
    });

});
