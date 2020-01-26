$(document).ready(function () {
    $(function () {
        $('#id_part_unit.select').select2();
        $('#id_footprint.select').select2();
        $('#id_storage.select').select2();
        $('#id_category.select').select2();


        $('.formset_row-distributors_sku').formset({
            addText: 'Add one more SKU',
            deleteText: 'Remove this SKU',
            prefix: 'distributors_sku',
            formCssClass: 'dynamic-formset-distributors'
        });
        $('.formset_row-manufacturers_sku').formset({
            addText: 'Add one more SKU',
            deleteText: 'Remove this SKU',
            prefix: 'manufacturers_sku',
            formCssClass: 'dynamic-formset-manufacturers'
        });
        $('.formset_row-part_parameters_value').formset({
            addText: 'Add one more parameter',
            deleteText: 'Remove this parameter',
            prefix: 'part_parameters_value',
            formCssClass: 'dynamic-formset-parts-parameters',
            deleteContainerClass: 'delete-here'
        });
    });

    $(function () {
      $('[data-toggle="tooltip"]').tooltip()
    })
});