/** @odoo-module **/

import { registry } from "@web/core/registry"; // Use the correct import path for registry
import { titleService as originalTitleService } from "@web/core/browser/title_service"; // Import the original service


registry.category("services").remove("title");

export const customTitleService = {
    ...originalTitleService, // Extend the original service
    start() {
        const originalService = originalTitleService.start(); // Call the original start function
        const titleParts = {};

        function getParts() {
            return Object.assign({}, titleParts);
        }

        function setParts(parts) {
            for (const key in parts) {
                const val = parts[key];
                if (!val | val === "Odoo") {
                    delete titleParts[key];
                } else {
                    titleParts[key] = val;
                }
            }

            // Custom logic to modify the title, e.g., adding a prefix
            document.title = Object.values({ "Librarian": "Librarian", ...titleParts }).join(" - ");
        }

        return {
            get current() {
                return document.title;
            },
            getParts,
            setParts,
        };
    },
};

// Register the custom service, overriding the original one
registry.category("services").add("title", customTitleService);
