$(document).ready(function () {
    $(function () {
        $('#id_part_unit.select').select2();
        $('#id_footprint.select').select2();
        $('#id_storage.select').select2();
        $('#id_category.select').select2();


        $('.formset_row-distributors_sku').formset({
            addText: 'add one',
            deleteText: 'remove',
            prefix: 'distributors_sku',
            formCssClass: 'dynamic-formset-distributors'
        });
        $('.formset_row-manufacturers_sku').formset({
            addText: 'add one',
            deleteText: 'remove',
            prefix: 'manufacturers_sku',
            formCssClass: 'dynamic-formset-manufacturers'
        });
        $('.formset_row-part_parameters_value').formset({
            addText: 'add one',
            deleteText: 'remove',
            prefix: 'part_parameters_value',
            formCssClass: 'dynamic-formset-parts-parameters'
        });
    });
});