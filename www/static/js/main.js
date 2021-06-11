$(document).ready(function () {

    /********************************/
    /* Main procedure for page load */
    /********************************/

    // jQuery object definitions
    var $pages = $('.page');
    var $linkToPage = $('.link-to-page');
    var $minutesYearSelect = $('#select-year-minutes');
    var $stylesYearSelect = $('#select-year-styles');
    var $entriesContainer = $('#selected-competition-entries');
    var $stylesContainer = $('#selected-year-styles');
    var $minutesContainer = $('#minutes-list');
    var $leaderboardContainer = $('#selected-year-leaderboard');

    // render the initial competitions content after getting the competition years
    $.getJSON('../static/data/competition_years.txt', function(years) {
        renderYearSelect(years, $stylesYearSelect);
        renderLeaderboard();
        renderStyleTable();
        $entriesContainer.html('');
    });
    
    // render the initial minutes content after getting the minutes years
    $.getJSON('../static/data/minutes_years.txt', function(years) {
        renderYearSelect(years, $minutesYearSelect);
        renderMinutes();
    });

    // show/hide content according to URL
    activatePage();

    // prepare document for user interaction
    attachEventHandlers();


    /******************************************/
    /* Functions used above are defined below */
    /******************************************/
    
    /**Get the hash from the URL and show/hide content appropriately
    */
    function activatePage() {
        // get the hash from the url
        var hash = window.location.hash ? window.location.hash.substring(1) : 'home';
        
        // add or remove active/inactive classes based on which "page" was selected
        $pages.each(function (idx, page) {
            if (page.id === hash) {
                $(page).removeClass('inactive')
                    .addClass('active');
            } else {
                $(page).removeClass('active')
                    .addClass('inactive');
            }
        });
    }

    /**Add event handlers for the document 
    */
    function attachEventHandlers() {
        // links to other "pages" will run the activatePage function to show/hide content
        $linkToPage.on('click', function () {
            // wait 0.1s before activating new page, otherwise hash might not be available
            setTimeout(activatePage, 100);
        });
        
        // selecting year for the minutes page will render the minutes list based on selection
        $minutesYearSelect.on('change', function () {
            renderMinutes();
        });

        // selecting year for competitions page renders leaderboard and style tables based on selection
        $stylesYearSelect.on('change', function () {
            renderLeaderboard();
            renderStyleTable();
            $entriesContainer.html('');
        });
    }

    /**Append years to a select object
     * @param  {array<int>} years - the values for the select
     * @param  {jQuery} $obj - the select object to append to
     */
    function renderYearSelect(years, $obj) {
        years.forEach(function (yr, idx) {
            let selected = '';
            if (idx === 0) selected = 'selected';
            $obj.append(`
                <option ${selected} value="${yr}">${yr}</option>
            `);
        });
    }
    
    /**Get brewer point totals for the selected year and render a table
     */
    function renderLeaderboard() {
        $leaderboardContainer.html('');

        let selectedYear = $stylesYearSelect.find('option:selected').val();
        
        $.getJSON(`../static/data/${selectedYear}/totals.txt`, function(totals) {
            let $tbl = $('<table class="table table-responsive"></table>');
            let $thead = $('<thead><tr><th>Place</th><th>Brewer</th><th>Points</th></tr></thead>');
            let $tbody = $('<tbody></tbody>');

            totals.forEach(entry => {
                $tbody.append(`<tr><td>${entry.Place}</td><td>${entry.Name}</td><td>${entry.Points}</td></tr>`)
            });

            $leaderboardContainer.append([
                `<h3 class="mb-3">${selectedYear} Leaderboard</h3>`, 
                $tbl.append($thead, $tbody)
            ]);
        });
    }
    
    /**Get competition styles for the selected year and render a table
     */
    function renderStyleTable() {
        let selectedYear = $stylesYearSelect.find('option:selected').val();

        let $tbl = $('<table id="style-table" class="table table-hover table-responsive"></table>')
        let $thead = $('<thead><tr><th>Month</th><th>Style</th></tr></thead>');
        let $tbody = $('<tbody></tbody>');

        $stylesContainer.html('');

        $.getJSON(`../static/data/${selectedYear}/competitions.txt`, function(comps) {
            comps.forEach((comp) => {
                let $row = $(`<tr><td>${comp.Month}</td><td>${comp.Style}</td></tr>`)

                // attach event handler to each row to show competition entries when clicked
                $row.on('click', function (){
                    $(this).siblings('tr').removeClass('active');
                    $(this).addClass('active');

                    renderEntries(comp);
                })
    
                $tbody.append($row);
            });

            $stylesContainer.append([
                `<h3 class="mb-0">${selectedYear} Competitions</h3>`,
                '<div class="mb-3"><small class="text-muted ml-2 mb-5">Select a competition to view the entries.</small></div>',
                $tbl.append($thead, $tbody)
            ]);
        });
    }
    
    /**Take a competition and render its entries in a table
     * @param  {dictionary} comp - The competition to render entries for
     */
    function renderEntries(comp) {
        $entriesContainer.html('');

        let $tbl = $('<table class="table"></table>');
        let $thead = $('<thead><tr><th>Brewer</th><th>Beer</th><th>Points</th></tr></thead>');
        let $tbody = $('<tbody></tbody>');

        if (comp.Entries === undefined || comp.Entries.length == 0) {
            $tbody.append('<tr><td colspan="3">No entries recorded</td></tr>')
        } else {
            comp.Entries.forEach(entry => {
                $tbody.append(`<tr><td>${entry.Name}</td><td>${entry.Beer}</td><td>${entry.Points}</td></tr>`);
            });
        }

        $entriesContainer.append([
            `<h3 class="mb-4">${comp.Month} Entries</h3>`,
            $tbl.append($thead, $tbody)
        ]);
    }
    
    /**Get minutes files data for the selected year and render an unordered list (sorted by date)
     */
    function renderMinutes() {
        let selectedYear = $minutesYearSelect.find('option:selected').val();

        $minutesContainer.html('');

        $.getJSON(`../static/data/${selectedYear}/minutes.txt`, function(minutes) {
            minutes.forEach(function (min) {
                var $li = $(`
                    <a href="../static/minutes/${selectedYear}/${min.FileName}" 
                        target="_blank"
                        class="p-2 text-primary list-group-item list-group-item-action">
                        ${min.FormattedDate}
                    </a>
                `);
                $minutesContainer.append($li);
            });
        });
    }
});