async function createList() {
    const input = document.getElementById("list-name");
    const name = input.value.trim();

    if (!name) return;

    await fetch("/todo-list", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
    });

    input.value = "";
    window.location.reload();
}

async function deleteList() {
    const confirmed = confirm(
        "Are you sure you want to delete this list and all its entries?"
    );

    if (!confirmed) return;

    const res = await fetch(`/todo-list/${listId}`, {
        method: "DELETE"
    });

    if (res.ok) {
        window.location.href = "/";
    } else {
        alert("Failed to delete list");
    }
}

async function loadEntries(listId) {
    const res = await fetch(`/todo-list/${listId}/entries`);
    const entries = await res.json();

    const ul = document.getElementById("entries");
    ul.innerHTML = "";

    entries.forEach(e => {
        const li = document.createElement("li");
        li.innerHTML = `
            ${e.name}
            <button onclick="deleteEntry('${listId}', '${e.id}')">X</button>
        `;
        ul.appendChild(li);
    });
}

async function addEntry() {
    const name = document.getElementById("entry-name").value;

    await fetch(`/todo-list/${listId}/entry`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, description: "" })
    });

    loadEntries(listId);
}

async function deleteEntry(listId, entryId) {
    await fetch(`/todo-list/${listId}/entry/${entryId}`, {
        method: "DELETE"
    });

    loadEntries(listId);
}

document.addEventListener("DOMContentLoaded", () => {
if (typeof listId !== "undefined") {
    loadEntries(listId);
}
});