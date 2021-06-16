odoo.define('custom_vracoop.tour.pos',
    ['web_tour.tour', 'pos_container.tour.tare', 'pos_order_mgmt_container.tour.reprint'],
    function(require) {
        "use strict";

        var Tour = require('web_tour.tour');

        var pos_container_steps = Tour.tours['pos_container'].steps;
        var steps = pos_container_steps.concat(Tour.tours['pos_order_mgmt_container'].steps);


        Tour.register('custom_vracoop', {
            test: true,
            url: '/pos/web'
        }, steps);
    });