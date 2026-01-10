async function createList() {
    const name = document.getElementById("list-name").value;

    await fetch("/todo-list", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
    });

    location.reload();
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

if (typeof listId !== "undefined") {
    loadEntries(listId);
}