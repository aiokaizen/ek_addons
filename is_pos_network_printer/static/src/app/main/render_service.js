/** @odoo-module **/
/* global html2canvas */

const applyWhenMounted = async ({ el, container, callback }) => {
    const elClone = el.cloneNode(true);
    container.appendChild(elClone);
    const res = await callback(elClone);
    elClone.remove();
    return res;
};

export const customHtmlToCanvas = async (el, options) => {
    console.log("Custom htmlToCanvas called");
    el.classList.add(options.addClass || "");

    // Add any custom behavior or modifications here
    return await applyWhenMounted({
        el,
        container: document.querySelector(".render-container"),
        callback: async (el) =>
            await html2canvas(el, {
                height: Math.ceil(el.clientHeight) + 40,
                width: Math.ceil(el.clientWidth),
                scale: 1,
            }),
    });
};
