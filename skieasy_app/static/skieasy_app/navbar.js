$(document).ready(function() {

  // Check for click events on the navbar burger icon
  $(".navbar-burger").click(function() {

    $(".navbar-burger").toggleClass("is-active");
    $(".navbar-menu").toggleClass("is-active");

  });

  $("#dropdown-button").click(() => {
    $(".dropdown").toggleClass("is-active");
  });

  const tabs = $(".panel-tabs a");
  const tabsContent = $(".filter-panel");

  tabs.click((event) => {
    tabs.removeClass("is-active");

    const tab = $(event.target);
    const target = tab.data("target");
    tab.addClass("is-active");

    tabsContent.each((_index, content) => {
      if (content.id === target) {
        content.classList.remove("is-hidden");
      } else {
        content.classList.add("is-hidden")
      }
    });


  });

  // Initialize the carousel for each card
  $('.carousel').slick({
    autoplay: false,
    dots: true,
    arrows: true,
  });

  // Initialize all input of type date
  var calendars = bulmaCalendar.attach('#pick-up-calendar', {
    labelFrom: "Pick-Up",
    color: "info",
    showHeader: false,
  });

  calendars.push(bulmaCalendar.attach('#drop-off-calendar', {
    labelFrom: "Drop-Off",
    color: "info",
    showHeader: false,
  }));

  // Loop on each calendar initialized
  for(var i = 0; i < calendars.length; i++) {
    // Add listener to select event
    calendars[i].on('select', date => {
      console.log(date);
    });
  }

  // To access to bulmaCalendar instance of an element
  var element = document.querySelector('#my-element');
  if (element) {
    // bulmaCalendar instance is available as element.bulmaCalendar
    element.bulmaCalendar.on('select', function(datepicker) {
      console.log(datepicker.data.value());
    });
  }

});
