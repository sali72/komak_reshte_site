$(document).ready(function () {
    // Initial order update for sortable table
    updateOrder();

    // Initialize searchable dropdown and set event handlers
    initializeSelect2();
    handleExamGroupChange();
    handleProvinceChange();
    initializeSortableTable();
    handleClearList();
    handleDeleteButtons();

    // Initialize searchable field of study dropdown
    function initializeSelect2() {
        $('#id_field_of_study').select2({
            placeholder: "Search by field of study, university, or unique code",
            allowClear: true,
            ajax: {
                url: getFieldsOfStudyUrl,
                dataType: 'json',
                delay: 250,
                data: getSelect2Data,
                processResults: processSelect2Results
            }
        });
    }

    // Get data for select2 AJAX request
    function getSelect2Data(params) {
        return {
            q: params.term, // Search term
            province: $('#id_province').val(), // Selected province
            exam_group: $('#id_exam_group').val() // Selected exam group
        };
    }

    // Process results for select2 AJAX response
    function processSelect2Results(data) {
        return {
            results: $.map(data.results, function (item) {
                return {
                    id: item.id,
                    text: `${item.name} - ${item.university} (Code: ${item.unique_code})`
                };
            })
        };
    }

    // Clear field of study selection when exam group changes
    function handleExamGroupChange() {
        $('#id_exam_group').change(function () {
            $('#id_field_of_study').val(null).trigger('change');
        });
    }

    // Clear field of study selection when province changes
    function handleProvinceChange() {
        $('#id_province').change(function () {
            $('#id_field_of_study').val(null).trigger('change');
        });
    }

    // Handle exam group change
    $('#id_exam_group').change(onExamGroupChange);

    // Handle province change
    $('#id_province').change(onProvinceChange);

    // Event handler for exam group change
    function onExamGroupChange() {
        var examGroup = $(this).val();
        $.ajax({
            url: getFieldsOfStudyUrl,
            data: {
                exam_group: examGroup,
                province: $('#id_province').val() // Also include the selected province
            },
            success: updateFieldsOfStudy
        });
    }

    // Event handler for province change
    function onProvinceChange() {
        var province = $(this).val();
        $.ajax({
            url: getFieldsOfStudyUrl,
            data: {
                province: province,
                exam_group: $('#id_exam_group').val() // Also include the selected exam group
            },
            success: updateFieldsOfStudy
        });
    }

    // Update field of study dropdown options
    function updateFieldsOfStudy(data) {
        var $fieldOfStudy = $('#id_field_of_study');
        $fieldOfStudy.empty(); // Clear previous options
        $fieldOfStudy.append('<option value="">None</option>'); // Add the default option
        $.each(data.fields_of_study, function (index, field) {
            var displayText = `${field.name} - ${field.university} (Code: ${field.unique_code})`;
            $fieldOfStudy.append('<option value="' + field.id + '">' + displayText + '</option>');
        });
    }

    // Initialize sortable table
    function initializeSortableTable() {
        new Sortable(document.getElementById('sortable-table').getElementsByTagName('tbody')[0], {
            animation: 150,
            onEnd: function (evt) {
                updateOrder();
                saveOrder();
            }
        });
    }

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
                csrfmiddlewaretoken: csrfToken,
                ordered_data: JSON.stringify(orderedData)
            },
            success: function (response) {
                console.log(response.message);
            }
        });
    }

    // Clear the list
    function handleClearList() {
        $('#clear-list-btn').click(function () {
            if (confirm('Are you sure you want to clear the list?')) {
                $.ajax({
                    url: clearListUrl,
                    type: 'POST',
                    data: {
                        csrfmiddlewaretoken: csrfToken
                    },
                    success: function () {
                        location.reload();
                    }
                });
            }
        });
    }

    // Event listener for delete buttons
    function handleDeleteButtons() {
        $(document).on('click', '.delete-btn', function () {
            var $row = $(this).closest('tr');
            var id = $row.data('id');
            $.ajax({
                url: deleteItemUrl + id + '/',
                type: 'POST',
                data: {
                    csrfmiddlewaretoken: csrfToken
                },
                success: function () {
                    $row.remove();
                    updateOrder(); // Update order numbers after deletion
                }
            });
        });
    }
});
