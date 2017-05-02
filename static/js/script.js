$(function () {
    var $predictForm = $('#predict-form');
    var $submitBtn = $('#submit-btn');
    var $resultBox = $('#result');

    var DelayGenie = {
        init: function () {
            DelayGenie._initEventHandlers();
            $('#calendar-input').calendar({
                firstDayOfWeek: 1,
                today: true,
                touchReadonly: false,
                ampm: false,
                disableMinute: true
            });
        },

        _initEventHandlers: function () {
            $predictForm.on('submit', DelayGenie._handleFormSubmit);
        },

        _handleFormSubmit: function (event) {
            event.preventDefault();
            DelayGenie._toggleLoadingButton(true);
            DelayGenie._toggleResultBox(false);
            $predictForm.form('reset');

            $.ajax({
                method: 'post',
                url: '/predict',
                data: JSON.stringify({
                    departure: {
                        lat: '',
                        lon: ''
                    },
                    arrival: {
                        lat: '',
                        lon: ''
                    },
                    date: ''
                }),
                contentType: 'application/json'
            }).done(function (data) {
                console.log('done', data);
            }).fail(function (data) {
                console.log('fail', data);
            }).always(function (data) {
                DelayGenie._toggleLoadingButton(false);
                DelayGenie._toggleResultBox(true);
            })
        },

        _toggleLoadingButton: function (enable) {
            $submitBtn.toggleClass('loading', enable);
        },

        _toggleResultBox: function (enable) {
            if (enable) {
                $resultBox.slideDown();
            } else {
                $resultBox.slideUp();
            }
        }
    };

    DelayGenie.init();
});