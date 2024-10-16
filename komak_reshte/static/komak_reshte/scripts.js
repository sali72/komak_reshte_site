$(document).ready(function () {
    updateOrder();  // Initial order update

    $('#id_province').change(function () {
        var province = $(this).val();
        $.ajax({
            url: getFieldsOfStudyUrl,
            data: {
                'province': province
            },
            success: function (data) {
                updateFieldsOfStudy(data.fields_of_study);
            }
        });
    });

    function updateFieldsOfStudy(fields_of_study) {
        var $fieldOfStudy = $('#id_field_of_study');
        $fieldOfStudy.empty(); // Clear previous options
        $fieldOfStudy.append('<option value="">None</option>'); // Add the default option
        $.each(fields_of_study, function (index, field) {
            var displayText = `${field.name} - ${field.university} (Code: ${field.unique_code})`;
            $fieldOfStudy.append('<option value="' + field.id + '">' + displayText + '</option>');
        });
    }

    // Initialize Sortable
    new Sortable(document.getElementById('sortable-table').getElementsByTagName('tbody')[0], {
        animation: 150,
        onEnd: function (evt) {
            updateOrder();
            saveOrder();
        }
    });

    // Update the order column without removing the icon
    function updateOrder() {
        $('#sortable-table tbody tr').each(function (index) {
            $(this).find('td .order-index').text(index + 1);  // Only update the order number
        });
    }

    // Save the order to the server
    function saveOrder() {
        var orderedData = [];
        $('#sortable-table tbody tr').each(function () {
            var id = $(this).data('id');
            orderedData.push(id);
        });
        $.ajax({
            url: updateOrderUrl,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrfToken,
                'ordered_data': JSON.stringify(orderedData)
            },
            success: function (response) {
                console.log(response.message);
            }
        });
    }

    // Clear the list
    $('#clear-list-btn').click(function () {
        if (confirm('Are you sure you want to clear the list?')) {
            $.ajax({
                url: clearListUrl,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrfToken
                },
                success: function () {
                    location.reload();
                }
            });
        }
    });
});
