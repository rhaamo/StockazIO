$(document).ready(function () {
    $(function () {
        // main add form
        $('#id_part_unit.select').select2();
        $('#id_footprint.select').select2();
        $('#id_storage.select').select2();
        $('#id_category.select').select2();
        // formsets can't have select2


        // dynamic formset handling
        $('.formset_row-distributors_sku').formset({
            addText: 'Add one more distributor SKU',
            deleteText: 'Remove this distributor SKU',
            prefix: 'distributors_sku',
            formCssClass: 'dynamic-formset-distributors',
            deleteContainerClass: 'delete-here-distrib'
        });
        $('.formset_row-manufacturers_sku').formset({
            addText: 'Add one more manufacturer SKU',
            deleteText: 'Remove this manufacturer SKU',
            prefix: 'manufacturers_sku',
            formCssClass: 'dynamic-formset-manufacturers',
            deleteContainerClass: 'delete-here-manuf'
        });
        $('.formset_row-part_parameters_value').formset({
            addText: 'Add one more parameter',
            deleteText: 'Remove this parameter',
            prefix: 'part_parameters_value',
            formCssClass: 'dynamic-formset-parts-parameters',
            deleteContainerClass: 'delete-here-partparam'
        });
    });

    // global tooltip magic
    $(function () {
      $('[data-toggle="tooltip"]').tooltip()
    })
});