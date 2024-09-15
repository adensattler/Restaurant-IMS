$(document).ready(function () {
    // Function to handle click event on table rows
    $('.edit-menu-item').click(function () {
        var editMenuItemId = $(this).data('item-id'); // Retrieve item ID from data attribute
        console.log(editMenuItemId);
        $.ajax({
            url: '/get_menu_item_details', // Flask route to handle the request
            method: 'POST',
            data: {editMenuItemId: editMenuItemId},
            success: function (response) {
                // Populate form fields with fetched menu item details  
                $('#editMenuItemID').val(response.menu_item_id);
                $('#editMenuItemName').val(response.name);
                $('#editMenuItemDescription').val(response.description);
                $('#editMenuItemCategory').val(response.category_name);

                // Clear existing components
                $('#menuItemComponentsList').empty();

                // Populate menu item components
                response.components.forEach(function(component) {
                    $('#menuItemComponentsList').append(`
                        <li>
                            ${component.inventory_item_name} (${component.unit_abbreviation}) – 
                            ${component.quantity_required} 
                            <button class="btn btn-sm btn-danger remove-component" 
                                    data-inventory-item-id="${component.inventory_item_id}">
                                X
                            </button>
                        </li>
                    `);
                });
            }
        });
    });



    // Add new component
    $('#addComponentBtn').click(function () {
        var menu_item_id = $('#editMenuItemID').val();
        var inventory_item_id = $('#newComponent').val();
        var quantity_required = $('#newQuantity').val();

        $.ajax({
            url: '/add_menu_item_component',
            method: 'POST',
            data: {
                menu_item_id: menu_item_id,
                inventory_item_id: inventory_item_id,
                quantity_required: quantity_required
            },
            success: function (response) {
                if (response.status === 'success') {
                    // Optionally update the UI
                    $('#menuItemComponentsList').append(
                        `<li>${$('#newComponent option:selected').text()} – ${quantity_required} 
                        <button class="btn btn-danger remove-component" data-inventory-item-id="${inventory_item_id}">X</button></li>`
                    );
                }
            }
        });
    });

// Delete component
$('#menuItemComponentsList').on('click', '.remove-component', function () {
    var menu_item_id = $('#editMenuItemID').val();
    var inventory_item_id = $(this).data('inventory-item-id');
    var componentElement = $(this).closest('li'); // Cache the list item element
    
    $.ajax({
        url: '/delete_menu_item_component',
        method: 'POST',
        data: {
            menu_item_id: menu_item_id,
            inventory_item_id: inventory_item_id
        },
        success: function (response) {
            if (response.status === 'success') {
                // Remove the component from the UI
                componentElement.remove();
            } else {
                console.error('Failed to delete component:', response);
            }
        },
        error: function (xhr, status, error) {
            console.error('Error deleting component:', error);
        }
    });
});
});
