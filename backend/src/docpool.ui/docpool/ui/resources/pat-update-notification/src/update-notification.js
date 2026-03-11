import { BasePattern } from "@patternslib/patternslib/src/core/basepattern";
import Parser from "@patternslib/patternslib/src/core/parser";
import registry from "@patternslib/patternslib/src/core/registry";

export const parser = new Parser("update-notification");
parser.addArgument("example-option", "Stranger");

class Pattern extends BasePattern {
    static name = "update-notification";
    static trigger = ".pat-update-notification";
    static parser = parser;

    async init() {
        if (window.__patternslib_import_styles) {
            // Only import styles if the global flag is set.
            // import("./update-notification.scss");
            // Include notification styles as its not bundled with the pattern.
            import("./_notification.scss");
        }

        // Try to avoid jQuery, but here is how to import it.
        // eslint-disable-next-line no-unused-vars
        const $ = (await import("jquery")).default;

        // Custom code
        const el = document.getElementById("dokpool-listing");
        const modified_since = el.dataset.listingModified;
        let pollingInterval = null;
        let hasNewData = false;
        console.log(modified_since);

        function checkForNewData() {
            let baseUrl = document.body.dataset.portalUrl;
            return fetch(baseUrl + "/@new-data-check", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                body: JSON.stringify({ modified_since: modified_since }),
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error(
                            `HTTP Error: ${response.status} ${response.statusText}`
                        );
                    }
                    return response.json();
                })
                .then((result) => {
                    if (result.modified_last > modified_since) {
                        showNewDataNotification();
                        hasNewData = true;
                    }
                    console.log(result.modified_last);
                    return result.modified_last;
                })
                .catch((error) => {
                    console.error("Fehler beim Prüfen auf neue Daten:", error);
                });
        }
        function refreshData() {
            window.location.reload();
        }
        // Polling starten
        pollingInterval = setInterval(() => {
            console.log("Polling...");
            checkForNewData();
        }, 10000);

        // The options are automatically created, if parser is defined.
        const example_option = this.options.exampleOption;

        function showNewDataNotification() {
            if (document.querySelector(".pat-notification")) {
                console.log("Notification already exists");
                return;
            } else {
                document.body.insertAdjacentHTML(
                    "beforeend",
                    '    <p class="pat-notification" data-pat-notification="type: banner">Neue Daten verfügbar! \n' +
                        '            <button\n id="refresh-data-btn"' +
                        '              class="btn btn-link ">' +
                        "              Jetzt aktualisieren\n" +
                        "            </button>\n</p>"
                );
                document
                    .getElementById("refresh-data-btn")
                    .addEventListener("click", refreshData);
                registry.scan($("[data-pat-notification]"));
            }
        }
    }
}

// Register Pattern class in the global pattern registry and make it usable there.
registry.register(Pattern);

// Export Pattern as default export.
// You can import it as ``import AnyName from "./update-notification";``
export default Pattern;
// Export BasePattern as named export.
// You can import it as ``import { Pattern } from "./update-notification";``
export { Pattern };
