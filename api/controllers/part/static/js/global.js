$(document).ready(function () {
    $(function () {
        // https://harvesthq.github.io/chosen/options.html
        // Forcing some defaults
        let chosenOpts = {
            disable_search: false,
            enable_split_word_search: true,
            search_contains: true,
            case_sensitive_search: false
        };
        $('#id_part_unit.select').chosen(chosenOpts);
        $('#id_footprint.select').chosen(chosenOpts);
        $('#id_storage.select').chosen(chosenOpts);
        $('#id_category.select').chosen(chosenOpts);
    });
});