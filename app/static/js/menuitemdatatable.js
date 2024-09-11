// new DataTable('#example', {
//     paging: true,
//     colReorder: true,
//     select: {
//         style: 'os',
//         selector: 'td:first-child'
//     },
// });

$(document).ready(function() {
    console.log("Document ready function started");

    var table = new DataTable('#itemTable', {
        paging: false,
        colReorder: true,
        select: {
            style: 'os',
            selector: 'td:first-child'
        },
        columnDefs: [
            {
                targets: 0,
                orderable: false,
                className: 'select-checkbox'
            },
            {
                targets: -1,
                orderable: false
            },
            // Hide some columns by default
            // {
            //     targets: [1],
            //     visible: false
            // }
        ],
        order: [[2, 'asc']], // Sort by Name column by default
        buttons: [
            {
                extend: 'colvis',
                text: 'Column Visibility',
                className: 'btn btn-sm btn-outline-secondary',
                columns: ':not(:first-child):not(:last-child)' // Exclude checkbox and actions columns
            },
            {
                extend: 'excel',
                text: 'Export',
                className: 'btn btn-sm btn-outline-secondary'
            },
        ],
        dom: 'lrtip' // This removes the default button and search placement
    });

    // Move buttons to the custom placeholder
    table.buttons().container().appendTo('#datatablesButtons');

    // Create and move search input to the custom placeholder
    $('#datatablesSearch').html('<input class="form-control mr-sm-2" type="search" placeholder="Search..." aria-label="Search">');
    

    $('#datatablesSearch input').on('keyup', function() {
        table.search(this.value).draw();
    });

    // ... (rest of code for select all functionality)
});