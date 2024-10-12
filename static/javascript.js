// Fichier : import-csv.js

// Fonction pour limiter le nombre de colonnes affichées
function limitColumns(maxColumns) {
    var table = document.getElementById("csvTable");

    if (!table) {
        return; // Exit the function if the table doesn't exist
    }

    var rows = table.getElementsByTagName("tr");
    // Check if there are any rows
    if (rows.length === 0) {
        console.warn("No rows found in the table.");
        return; // Exit the function if there are no rows
    }

    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName("td");
        for (var j = maxColumns; j < cells.length; j++) {
            cells[j].style.display = "none";
        }
    }
}

// Fonction pour limiter le nombre de lignes affichées
function limitRows(maxRows) {
    var table = document.getElementById("csvTable");
        // Check if the table exists
    if (!table) {
        return; // Exit the function if the table doesn't exist
    }

    var rows = table.getElementsByTagName("tr");
        // Check if there are any rows
    if (rows.length === 0) {
        console.warn("No rows found in the table.");
        return; // Exit the function if there are no rows
    }

    for (var i = maxRows; i < rows.length; i++) {
        rows[i].style.display = "none";
    }
}

// Appeler les fonctions pour limiter les colonnes et les lignes au chargement de la page
window.onload = function() {
    var maxColumns = 5;  // Nombre maximal de colonnes à afficher
    var maxRows = 1;    // Nombre maximal de lignes à afficher
    limitColumns(maxColumns);
    limitRows(maxRows);
};
