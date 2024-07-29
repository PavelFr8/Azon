// static/js/base.js

$(document).ready(function() {
    // Automatically hide flash messages after 5 seconds
    setTimeout(function() {
        $('.flashes .alert').fadeOut('slow', function() {
            $(this).remove();
        });
    }, 5000);

    // Manually hide flash messages on close button click
    $('.flashes .alert .close').on('click', function() {
        $(this).closest('.alert').fadeOut('slow', function() {
            $(this).remove();
        });
    });

    // Initialize Slick slider
    $('.category-slider').slick({
        infinite: true,
        slidesToShow: 5, // Количество видимых элементов
        slidesToScroll: 1,
        speed: 500, // Плавность перелистывания
        prevArrow: '<button type="button" class="slick-prev"><i class="fas fa-chevron-left" style="color: black;"></i></button>',
        nextArrow: '<button type="button" class="slick-next"><i class="fas fa-chevron-right" style="color: black;"></i></button>',
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1,
                    infinite: true,
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                    arrows: false // Отключение кнопок навигации на мобильных устройствах
                }
            }
        ]
    });
});