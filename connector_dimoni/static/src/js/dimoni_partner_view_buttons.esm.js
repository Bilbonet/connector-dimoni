/* @odoo-module */
import {KanbanController} from "@web/views/kanban/kanban_controller";
import {ListController} from "@web/views/list/list_controller";
import {kanbanView} from "@web/views/kanban/kanban_view";
import {listView} from "@web/views/list/list_view";
import {registry} from "@web/core/registry";

class DimoniPartnerListController extends ListController {
    onImportFromDimoniClick() {
        this.actionService.doAction(
            "connector_dimoni.action_dimoni_partner_import_wizard"
        );
    }
}

DimoniPartnerListController.template = "connector_dimoni.DimoniPartnerList.Buttons";

const DimoniPartnerListView = {
    ...listView,
    Controller: DimoniPartnerListController,
};

registry
    .category("views")
    .add("dimoni_partner_import_button_list", DimoniPartnerListView);

class DimoniPartnerKanbanController extends KanbanController {
    onImportFromDimoniClick() {
        this.actionService.doAction(
            "connector_dimoni.action_dimoni_partner_import_wizard"
        );
    }
}

DimoniPartnerKanbanController.template =
    "connector_dimoni.DimoniPartnerKanban.Buttons";

const DimoniPartnerKanbanView = {
    ...kanbanView,
    Controller: DimoniPartnerKanbanController,
};

registry
    .category("views")
    .add("dimoni_partner_import_button_kanban", DimoniPartnerKanbanView);
