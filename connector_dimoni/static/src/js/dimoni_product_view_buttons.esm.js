/* @odoo-module */
import {KanbanController} from "@web/views/kanban/kanban_controller";
import {ListController} from "@web/views/list/list_controller";
import {kanbanView} from "@web/views/kanban/kanban_view";
import {listView} from "@web/views/list/list_view";
import {registry} from "@web/core/registry";

class DimoniProductListController extends ListController {
    onImportFromDimoniClick() {
        this.actionService.doAction(
            "connector_dimoni.action_dimoni_product_import_wizard"
        );
    }
}

DimoniProductListController.template = "connector_dimoni.DimoniProductList.Buttons";

const DimoniProductListView = {
    ...listView,
    Controller: DimoniProductListController,
};

registry.category("views").add("dimoni_import_button_list", DimoniProductListView);

class DimoniProductKanbanController extends KanbanController {
    onImportFromDimoniClick() {
        this.actionService.doAction(
            "connector_dimoni.action_dimoni_product_import_wizard"
        );
    }
}

DimoniProductKanbanController.template = "connector_dimoni.DimoniProductKanban.Buttons";

const DimoniProductKanbanView = {
    ...kanbanView,
    Controller: DimoniProductKanbanController,
};

registry.category("views").add("dimoni_import_button_kanban", DimoniProductKanbanView);
