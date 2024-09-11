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
                    $('#menuItemComponentsList').append(
                        `<li>${component.inventory_item_name} - ${component.quantity_required}/${component.unit}</li>`
                    );
                });
            }
        });
    });
});
