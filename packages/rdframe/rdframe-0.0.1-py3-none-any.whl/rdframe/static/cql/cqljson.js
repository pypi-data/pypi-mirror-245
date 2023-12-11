function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

function setupEditorAutoUpdate(editor, cql_name, column) {
    editor.on("change", debounce(async function () {
        const content = editor.getValue();

        try {
            const response = await fetch(`${CONFIG.BACKEND_ENDPOINT}/cqljson-update/${cql_name}/${column}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'text/plain'
                },
                body: content
            });

            if (response.ok) {
                console.log(`Successfully updated ${cql_name} ${column}; attempting to update the results...`);
                const columns_to_update = ['sparql', 'results'];
                for (const col of columns_to_update) {
                    const targetEditor = editorsMap[cql_name].find(e => e.getTextArea().id === `${cql_name}_${col}`);
                    if (targetEditor) {
                        await updateEditorWithData(cql_name, col, targetEditor);
                    }
                }
            } else {
                console.error(`Failed to update ${cql_name} ${column}. Status: ${response.status}`);
            }
        } catch (error) {
            console.error(`Error updating ${cql_name} ${column}`, error);
        }
    }, 250)); // The function will be executed 250 ms after the last change event
}

async function updateEditorWithData(cql_name, column, editor) {
    try {
        const responseData = await fetch(`${CONFIG.BACKEND_ENDPOINT}/cqljson/${cql_name}/${column}`, {mode: 'cors'});
        const data = await responseData.text();

        editor.setValue(data);

        setTimeout(function () {
            editor.refresh();
        }, 1);
    } catch (error) {
        console.error("Error updating editor with data: ", error);
    }
}


let editorsMap = {};

async function updateEditorWithData(cql_name, column, editor) {
    try {
        const responseData = await fetch(`${CONFIG.BACKEND_ENDPOINT}/cqljson/${cql_name}/${column}`, {mode: 'cors'});
        const data = await responseData.text();
        editor.setValue(data);
        setTimeout(() => editor.refresh(), 1);
    } catch (error) {
        console.error("Error updating editor with data: ", error);
    }
}

async function populateCQL() {
    try {
        const response = await fetch(`${CONFIG.BACKEND_ENDPOINT}/cqljson`);
        const cqlNames = await response.json();

        const sidebar = document.getElementById('sidebar');
        const content = document.getElementById('content');

        for (const cql_name of cqlNames) {
            const index = cqlNames.indexOf(cql_name);
            const isActive = index === 0;

            // Create the tab list item
            const tabListItem = document.createElement('li');
            tabListItem.className = `tab ${isActive ? 'active' : ''}`;
            const tabButton = document.createElement('a');
            tabButton.href = `#${cql_name}_content`;
            tabButton.innerText = cql_name;
            tabButton.addEventListener('click', (event) => {
                event.preventDefault();
                document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
                document.querySelectorAll('.tab-content-pane').forEach(pane => pane.style.display = 'none');

                tabListItem.classList.add('active');
                const contentPane = document.getElementById(`${cql_name}_content`);
                if (contentPane) {
                    contentPane.style.display = 'block';
                }
            });
            tabListItem.appendChild(tabButton);
            sidebar.appendChild(tabListItem);

            // Create the content pane
            const cqlContentPane = document.createElement('div');
            cqlContentPane.id = `${cql_name}_content`;
            cqlContentPane.className = `tab-content-pane`;
            cqlContentPane.style.display = isActive ? 'block' : 'none';
            content.appendChild(cqlContentPane);


            const columns = ['cql', 'sparql', 'example_data', 'results'];
            let topRow = document.createElement('div');
            topRow.className = 'row';
            let bottomRow = document.createElement('div');
            bottomRow.className = 'row';

            for (const column of columns) {
                const quadrantDiv = document.createElement('div');
                quadrantDiv.className = 'col s6'; // This should be adjusted if you want equal space considering the sidebar
                // const columnDiv = document.createElement('div');
                // columnDiv.className = 'col s6';

                const title = document.createElement('h5');
                title.innerText = column.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
                quadrantDiv.appendChild(title);

                const textArea = document.createElement('textarea');
                textArea.id = `${cql_name}_${column}`;
                quadrantDiv.appendChild(textArea);

                const editorMode = column === 'cql' ? 'application/ld+json' : (column === 'sparql' ? 'sparql' : 'turtle');
                const isReadOnly = column === 'sparql';

                const editor = CodeMirror.fromTextArea(textArea, {
                    mode: editorMode,
                    lineWrapping: true,
                    readOnly: isReadOnly,
                    foldOptions: {
                        rangeFinder: CodeMirror.fold.prefix,
                        widget: "..."
                    },
                    autoRefresh: true
                });

                if (!editorsMap[cql_name]) {
                    editorsMap[cql_name] = [];
                }
                editorsMap[cql_name].push(editor);

                await updateEditorWithData(cql_name, column, editor);

                if (['cql', 'sparql'].includes(column)) {
                    topRow.appendChild(quadrantDiv);
                } else {
                    bottomRow.appendChild(quadrantDiv);
                }

                if (['cql', 'example_data'].includes(column)) {
                    setupEditorAutoUpdate(editor, cql_name, column);
                }

            }

            cqlContentPane.appendChild(topRow);
            cqlContentPane.appendChild(bottomRow);
            // cqlContainer.appendChild(cqlTabePane);
        }

    } catch (error) {
        console.error("Error populating CQL: ", error);
    }
}


document.addEventListener('DOMContentLoaded', async function () {
    await populateCQL();
    // Initialize the tabs
    setTimeout(() => {
        const elems = document.querySelectorAll('.tabs');
        M.Sidenav.init(elems);
    }, 0);
});
