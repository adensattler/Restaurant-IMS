// JavaScript to set the item name in the modal
document.querySelectorAll('.dropdown-item.text-danger').forEach(item => {
    item.addEventListener('click', event => {
        const itemName = item.getAttribute('data-item-name');
        const itemId = item.getAttribute('data-item-id');
        document.getElementById('itemNameToDelete').textContent = itemName;
        document.getElementById('itemIdInput').value = itemId;
    });
});

$(document).ready(function () {
    // Function to handle click event on table rows
    $('.edit-item').click(function () {
        var editItemId = $(this).data('item-id'); // Retrieve item ID from data attribute
        console.log(editItemId)
        $.ajax({
            url: '/get_item_details', // Flask route to handle the request
            method: 'POST',
            data: {editItemId: editItemId},
            success: function (response) {
                // Populate form fields with fetched item details  
                $('#editItemID').val(response.inventory_item_id);
                $('#editItemName').val(response.name);
                $('#editItemDescription').val(response.description);
                $('#editItemLocation').val(response.location_id);
                $('#editItemGTIN').val(response.GTIN);
                $('#editItemSKU').val(response.SKU);
                $('#editItemUnit').val(response.unit);
                $('#editItemWeight').val(response.weight);
                $('#editItemPrice').val(response.price);
                $('#editItemStock').val(response.stock);
                $('#editItemLowStockLevel').val(response.low_stock_level);

            }
        });
    });
});