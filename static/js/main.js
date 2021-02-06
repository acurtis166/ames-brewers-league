$(document).ready(function () {

    // Initialize variables
    // 'Data' object comes from data.js file
    var pages = $('.page');
    var minutesPath = '../static/minutes/';

    // render the minutes list
    Data.Minutes.forEach(function (min) {
        var li = $(`
            <a href="${minutesPath}${min.FileName}" 
                target="_blank"
                class="p-2 text-primary list-group-item list-group-item-action">
                ${min.FormattedDate}
            </a>
        `);
        $('#minutes-list').append(li);
    });

    // render the year select
    Data.DistinctYears.forEach(function (yr, idx) {
        let selected = '';
        if (idx === 0) selected = 'selected';
        $('#select-year-styles').append(`
            <option ${selected} value="${yr}">${yr}</option>
        `);
    });

    // Initialize site
    activatePage();
    attachEventHandlers();
    renderLeaderboard();
    renderStyleTable();
    clearEntries();

    // Functions
    function activatePage() {
        var hash = window.location.hash ? window.location.hash.substring(1) : 'home';
        pages.each(function (idx, page) {
            if (page.id === hash) {
                $(page).removeClass('inactive')
                    .addClass('active');
            } else {
                $(page).removeClass('active')
                    .addClass('inactive');
            }
        });
    }

    function attachEventHandlers() {
        $('.link-to-page').on('click', function () {
            setTimeout(activatePage, 100);
        });

        $('#minutes-search').on('keyup', function () {
            var term = $(this).val().toLowerCase();
            $('#minutes-list a').filter(function () {
                $(this).toggle($(this).text().toLowerCase().indexOf(term) > -1);
            });
        });

        $('#select-year-styles').on('change', function () {
            renderLeaderboard();
            renderStyleTable();
            clearEntries();
        });
    }

    function renderLeaderboard() {
        let container = $('#selected-year-leaderboard');
        container.html('');

        let selectedYear = $('#select-year-styles').find('option:selected').val();
        let leaderboard = Data.Leaderboards.filter(x => x.Year == selectedYear)[0];

        let listGroup = $('<ul class="list-group"></ul>');
        leaderboard.Entries.forEach((entry, idx) => {
            if (idx < 5) {
                listGroup.append(`
                    <li class="list-group-item d-flex justify-content-between w-100">
                        <span>${entry.Name}</span>
                        <span>${entry.Points} ${entry.Points > 1 ? 'points' : 'point'}</span>
                    </li>
                `);
            }
        });

        container.append([`<h3 class="mb-3">${selectedYear} Leaderboard</h3>`, listGroup]);
    }

    function renderStyleTable() {
        let container = $('#selected-year-styles');
        let selectedYear = $('#select-year-styles').find('option:selected').val();
        let ul = $('<ul class="list-group"></ul>');

        container.html('');

        getCompetitionsByYear(selectedYear).forEach(comp => {
            let item = $(`
                <li class="list-group-item list-group-item-action">
                    <div class="d-flex justify-content-between w-100">
                        <span>${comp.FormattedDate}</span>
                    </div>
                    <div class="d-flex justify-content-between w-100">
                        <span class="ml-2">${comp.Style} (${comp.Category})</span>
                    </div>
                </li>
            `);
            item.on('click', function () {
                $(this).siblings('li').removeClass('active');
                $(this).addClass('active');

                renderEntries(comp);
            });

            ul.append(item)
        });

        container.append([
            `<h3 class="mb-0">${selectedYear} Competitions</h3>`,
            '<div class="mb-3"><small class="text-muted ml-2 mb-5">Select a competition to view the entries.</small></div>',
            ul
        ]);
    }

    function renderEntries(comp) {
        let container = $('#selected-competition-entries');
        clearEntries();

        let listGroup = $('<ul class="list-group"></ul>');
        if (comp.Entries === undefined || comp.Entries.length == 0) {
            listGroup.append('<li class="list-group-item">No entries recorded</li>');
        } else {
            comp.Entries.forEach(entry => {
                listGroup.append(`
                    <li class="list-group-item">
                        <div class="d-flex justify-content-between w-100">
                            <span>${entry.Name}</span>
                            <small class="text-muted">${entry.Points || 0} ${entry.Points > 1 ? 'points' : 'point'}</small>
                        </div>
                        <div class="d-flex justify-content-between w-100">
                            <span class="text-muted">${entry.Beer || ''}</span>
                        </div>
                    </li>
                `);
            });
        }

        container.append([`<h3 class="mb-4">${comp.FormattedDate} Entries</h3>`, listGroup]);
    }

    function clearEntries() {
        let container = $('#selected-competition-entries');
        container.html('');
    }

    function getCompetitionsByYear(year) {
        return Data.Competitions.filter(comp => {
            return comp.Year == year;
        });
    }

});