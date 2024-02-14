// Fichier : import-csv.js

// Fonction pour limiter le nombre de colonnes affichées
function limitColumns(maxColumns) {
    var table = document.getElementById("csvTable");
    var rows = table.getElementsByTagName("tr");
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
    var rows = table.getElementsByTagName("tr");
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
