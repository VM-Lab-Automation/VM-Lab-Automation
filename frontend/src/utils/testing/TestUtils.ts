export function flushPromises() {
    return new Promise(resolve => setImmediate(resolve));
}

export function clickOn(el: HTMLElement) {
    el.dispatchEvent(new MouseEvent("click", { bubbles: true }));
}