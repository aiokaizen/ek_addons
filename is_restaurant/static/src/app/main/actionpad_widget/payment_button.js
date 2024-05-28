/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { ActionpadWidget } from "@point_of_sale/app/screens/product_screen/action_pad/action_pad";
import { FloorScreen } from "@pos_restaurant/app/floor_screen/floor_screen";


patch(FloorScreen.prototype, {
    async onSelectTable(table, ev) {
        if (!this.pos.isEditMode) {
            const hasServerGroup = await this.env.services.user.hasGroup(
                "is_restaurant.group_is_restaurant_server"
            )
            this.pos.userHasServerGroup = hasServerGroup;
        }
        super.onSelectTable(table, ev);
    }
});


patch(ActionpadWidget.prototype, {
    get displayPayOrderButton() {
        return !this.pos.userHasServerGroup;
    }
});
