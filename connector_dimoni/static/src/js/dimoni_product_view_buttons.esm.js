/* @odoo-module */
import {registry} from "@web/core/registry";
import {KanbanController} from "@web/views/kanban/kanban_controller";
import {kanbanView} from "@web/views/kanban/kanban_view";
import {ListController} from "@web/views/list/list_controller";
import {listView} from "@web/views/list/list_view";

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

DimoniProductKanbanController.template =
    "connector_dimoni.DimoniProductKanban.Buttons";

const DimoniProductKanbanView = {
    ...kanbanView,
    Controller: DimoniProductKanbanController,
};

registry
    .category("views")
    .add("dimoni_import_button_kanban", DimoniProductKanbanView);
